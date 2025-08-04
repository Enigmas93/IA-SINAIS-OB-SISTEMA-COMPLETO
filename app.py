from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit, join_room, leave_room
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import sys
from dotenv import load_dotenv
import logging
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Add current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Initialize Flask app with explicit template and static folders
# Use absolute paths to ensure templates are found in production
base_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, os.pardir))

app = Flask(
    __name__,
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates")),
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))
)

# Log template and static directories for debugging
logger = logging.getLogger(__name__)
logger.info(f"Template directory: {template_dir}")
logger.info(f"Static directory: {static_dir}")
logger.info(f"Template directory exists: {os.path.exists(template_dir)}")
logger.info(f"Static directory exists: {os.path.exists(static_dir)}")

# Check if index.html exists
index_template = os.path.join(template_dir, 'index.html')
logger.info(f"index.html path: {index_template}")
logger.info(f"index.html exists: {os.path.exists(index_template)}")

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Fix DATABASE_URL for Render (postgres:// -> postgresql://)
database_url = os.getenv('DATABASE_URL', 'sqlite:///trading_bot.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 24)))

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Make socketio available globally
app.socketio = socketio

# Configure logging
log_handlers = [logging.StreamHandler()]

# Only add file handler if logs directory exists or can be created
log_file = os.getenv('LOG_FILE', 'logs/trading_bot.log')
try:
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    log_handlers.append(logging.FileHandler(log_file))
except (OSError, PermissionError):
    # If we can't create log file, just use console logging
    pass

logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=log_handlers
)
logger = logging.getLogger(__name__)

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

# Import models and services after db initialization
try:
    from models import User, TradingConfig, TradeHistory, MLModel
    logger.info("Models imported successfully")
except ImportError as e:
    logger.error(f"Error importing models: {e}")
    # Create dummy models to prevent app crash
    class User:
        pass
    class TradingConfig:
        pass
    class TradeHistory:
        pass
    class MLModel:
        pass

# Import services with robust fallback system
try:
    from services import IQOptionService, SignalAnalyzer, TradingBot, MLService
    services_available = True
    logger.info("Services imported successfully")
except ImportError as e:
    logger.warning(f"Services not available during startup: {e}")
    services_available = False
    # Create minimal dummy services
    class IQOptionService:
        def __init__(self, *args, **kwargs):
            self.is_connected = False
            self.balance = 0.0
    class SignalAnalyzer:
        def __init__(self, *args, **kwargs):
            pass
    class TradingBot:
        def __init__(self, *args, **kwargs):
            self.is_running = False
    class MLService:
        def __init__(self, *args, **kwargs):
            pass

# Import and register routes blueprint
try:
    from src.routes import api, main
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(main)
    
    # Add debug route for template checking
    @app.route('/debug/templates')
    def debug_templates():
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(base_dir, 'templates')
        
        templates_info = {
            'base_dir': base_dir,
            'template_dir': template_dir,
            'template_dir_exists': os.path.exists(template_dir),
            'templates': []
        }
        
        if os.path.exists(template_dir):
            templates_info['templates'] = os.listdir(template_dir)
        
        return templates_info
    logger.info("Routes registered successfully")
except ImportError as e:
    logger.error(f"Error importing routes: {e}")
    # Create minimal routes to keep app running
    from flask import Blueprint
    api = Blueprint('api', __name__, url_prefix='/api')
    main = Blueprint('main', __name__)
    
    @main.route('/')
    def index():
        return "Application starting..."
    
    @api.route('/health')
    def health():
        return {'status': 'ok', 'services_available': services_available}
    
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(main)

# Global trading bot instance
trading_bot = None

def get_or_create_trading_bot():
    """Get or create trading bot instance"""
    global trading_bot
    if trading_bot is None:
        # Create a dummy bot for status checking
        class DummyBot:
            def get_bot_status(self, user_id):
                return {
                    'running': False,
                    'current_session': None,
                    'trades_today': 0,
                    'profit_today': 0.0,
                    'last_signal': None
                }
            
            def start_bot(self, user, config):
                global trading_bot
                trading_bot = TradingBot(user.id, config, app)
                return trading_bot.start()
            
            def stop_bot(self, user_id):
                global trading_bot
                if trading_bot and hasattr(trading_bot, 'stop'):
                    trading_bot.stop()
                    trading_bot = None
                    return True
                return False
        
        trading_bot = DummyBot()
    return trading_bot

# Main routes moved to routes.py blueprint

# Configuration endpoints moved to routes.py

@app.route('/api/iq-credentials', methods=['GET', 'POST'])
@jwt_required()
def iq_credentials():
    """Get or update IQ Option credentials"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'success': False, 'message': 'Usuário não encontrado'}), 404
    
    if request.method == 'GET':
        return jsonify({
            'success': True,
            'has_credentials': bool(user.iq_email and user.iq_password),
            'iq_email': user.iq_email or ''
        })
    
    # POST - Update credentials
    data = request.get_json()
    iq_email = data.get('iq_email')
    iq_password = data.get('iq_password')
    
    if not iq_email or not iq_password:
        return jsonify({'success': False, 'message': 'Email e senha são obrigatórios'}), 400
    
    user.iq_email = iq_email
    user.iq_password = iq_password
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Credenciais atualizadas com sucesso'})

# Bot control endpoints moved to routes.py

@app.route('/api/trades')
@jwt_required()
def get_trades():
    """Get trade history"""
    user_id = get_jwt_identity()
    
    # Get query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    
    query = TradeHistory.query.filter_by(user_id=user_id)
    
    if start_date:
        query = query.filter(TradeHistory.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(TradeHistory.timestamp <= datetime.fromisoformat(end_date))
    
    trades = query.order_by(TradeHistory.timestamp.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'trades': [{
            'id': trade.id,
            'timestamp': trade.timestamp.isoformat(),
            'asset': trade.asset,
            'direction': trade.direction,
            'amount': trade.amount,
            'result': trade.result,
            'profit': trade.profit,
            'martingale_level': trade.martingale_level,
            'signal_strength': trade.signal_strength
        } for trade in trades.items],
        'pagination': {
            'page': trades.page,
            'pages': trades.pages,
            'per_page': trades.per_page,
            'total': trades.total
        }
    })

# User profile endpoint moved to routes.py

@app.route('/api/dashboard/stats')
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics"""
    user_id = get_jwt_identity()
    
    # Get today's trades
    today = datetime.now().date()
    today_trades = TradeHistory.query.filter(
        TradeHistory.user_id == user_id,
        TradeHistory.timestamp >= today
    ).all()
    
    # Calculate stats
    total_trades_today = len(today_trades)
    wins_today = len([t for t in today_trades if t.result == 'win'])
    profit_today = sum([t.profit for t in today_trades])
    win_rate_today = (wins_today / total_trades_today * 100) if total_trades_today > 0 else 0
    
    return jsonify({
        'success': True,
        'stats': {
            'trades_today': total_trades_today,
            'wins_today': wins_today,
            'profit_today': profit_today,
            'win_rate_today': win_rate_today,
            'current_balance': 1000.0  # Placeholder - should come from IQ Option API
        }
    })

# WebSocket endpoint temporarily disabled to avoid 400 errors
# @app.route('/ws')
# def websocket_endpoint():
#     """WebSocket endpoint placeholder"""
#     return jsonify({'message': 'WebSocket endpoint - requires WebSocket implementation'}), 400

@app.route('/api/statistics')
@jwt_required()
def get_statistics():
    """Get trading statistics"""
    user_id = get_jwt_identity()
    
    # Get date range
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = TradeHistory.query.filter_by(user_id=user_id)
    
    if start_date:
        query = query.filter(TradeHistory.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(TradeHistory.timestamp <= datetime.fromisoformat(end_date))
    
    trades = query.all()
    
    if not trades:
        return jsonify({
            'success': True,
            'statistics': {
                'total_trades': 0,
                'wins': 0,
                'losses': 0,
                'win_rate': 0,
                'total_profit': 0,
                'best_streak': 0,
                'worst_streak': 0,
                'avg_profit_per_trade': 0
            }
        })
    
    total_trades = len(trades)
    wins = len([t for t in trades if t.result == 'win'])
    losses = total_trades - wins
    win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0
    total_profit = sum(t.profit for t in trades)
    avg_profit = total_profit / total_trades if total_trades > 0 else 0
    
    # Calculate streaks
    current_streak = 0
    best_streak = 0
    worst_streak = 0
    
    for trade in trades:
        if trade.result == 'win':
            current_streak = max(0, current_streak) + 1
            best_streak = max(best_streak, current_streak)
        else:
            current_streak = min(0, current_streak) - 1
            worst_streak = min(worst_streak, current_streak)
    
    return jsonify({
        'success': True,
        'statistics': {
            'total_trades': total_trades,
            'wins': wins,
            'losses': losses,
            'win_rate': round(win_rate, 2),
            'total_profit': round(total_profit, 2),
            'best_streak': best_streak,
            'worst_streak': abs(worst_streak),
            'avg_profit_per_trade': round(avg_profit, 2)
        }
    })

# Create application factory function
def create_app():
    return app

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
    
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting application on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
else:
    # For production deployment
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")