from datetime import datetime
import json
from database import db

class User(db.Model):
    """User model for authentication and user management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    
    # IQ Option credentials (stored in plain text for API access - consider encryption in production)
    iq_email = db.Column(db.String(120))
    iq_password = db.Column(db.Text)
    account_type = db.Column(db.String(10), default='PRACTICE')  # 'PRACTICE' or 'REAL'
    
    # Relationships
    trading_configs = db.relationship('TradingConfig', backref='user', lazy=True, cascade='all, delete-orphan')
    trade_history = db.relationship('TradeHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    ml_models = db.relationship('MLModel', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'

class TradingConfig(db.Model):
    """Trading configuration for each user"""
    __tablename__ = 'trading_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Asset configuration
    asset = db.Column(db.String(20), default='EURUSD')
    
    # Trade amount configuration
    trade_amount = db.Column(db.Float, default=10.0)
    use_balance_percentage = db.Column(db.Boolean, default=True)
    balance_percentage = db.Column(db.Float, default=2.0)  # 2% of balance
    
    # Risk management
    take_profit = db.Column(db.Float, default=70.0)  # Percentage
    stop_loss = db.Column(db.Float, default=30.0)    # Percentage
    
    # Martingale configuration
    martingale_enabled = db.Column(db.Boolean, default=True)
    max_martingale_levels = db.Column(db.Integer, default=3)
    martingale_multiplier = db.Column(db.Float, default=2.2)
    
    # Schedule configuration
    morning_start = db.Column(db.String(5), default='10:00')
    morning_end = db.Column(db.String(5), default='12:00')
    afternoon_start = db.Column(db.String(5), default='14:00')
    afternoon_end = db.Column(db.String(5), default='17:00')
    
    # Operation mode
    auto_mode = db.Column(db.Boolean, default=False)
    manual_mode = db.Column(db.Boolean, default=True)
    operation_mode = db.Column(db.String(10), default='manual')  # 'auto' or 'manual'
    
    # Signal analysis configuration
    rsi_period = db.Column(db.Integer, default=14)
    rsi_oversold = db.Column(db.Float, default=30.0)
    rsi_overbought = db.Column(db.Float, default=70.0)
    
    macd_fast = db.Column(db.Integer, default=12)
    macd_slow = db.Column(db.Integer, default=26)
    macd_signal = db.Column(db.Integer, default=9)
    
    ma_short_period = db.Column(db.Integer, default=20)
    ma_long_period = db.Column(db.Integer, default=50)
    
    aroon_period = db.Column(db.Integer, default=14)
    
    # Price action patterns
    enable_engulfing = db.Column(db.Boolean, default=True)
    enable_hammer = db.Column(db.Boolean, default=True)
    enable_doji = db.Column(db.Boolean, default=True)
    enable_shooting_star = db.Column(db.Boolean, default=True)
    
    # ML configuration
    use_ml_signals = db.Column(db.Boolean, default=True)
    ml_confidence_threshold = db.Column(db.Float, default=0.7)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<TradingConfig User:{self.user_id} Asset:{self.asset}>'

class TradeHistory(db.Model):
    """Trade history and results"""
    __tablename__ = 'trade_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Trade details
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    asset = db.Column(db.String(20), nullable=False)
    direction = db.Column(db.String(4), nullable=False)  # 'call' or 'put'
    amount = db.Column(db.Float, nullable=False)
    expiration_time = db.Column(db.Integer, default=60)  # seconds
    
    # Entry conditions
    entry_price = db.Column(db.Float)
    exit_price = db.Column(db.Float)
    
    # Results
    result = db.Column(db.String(10))  # 'win', 'loss', 'tie'
    profit = db.Column(db.Float, default=0.0)
    payout_percentage = db.Column(db.Float)
    
    # Martingale info
    martingale_level = db.Column(db.Integer, default=0)
    is_martingale = db.Column(db.Boolean, default=False)
    
    # Signal analysis data
    signal_strength = db.Column(db.Float)  # 0-1 confidence
    rsi_value = db.Column(db.Float)
    macd_value = db.Column(db.Float)
    macd_signal_value = db.Column(db.Float)
    ma_short_value = db.Column(db.Float)
    ma_long_value = db.Column(db.Float)
    aroon_up = db.Column(db.Float)
    aroon_down = db.Column(db.Float)
    
    # Price action patterns detected
    patterns_detected = db.Column(db.Text)  # JSON string of detected patterns
    
    # ML prediction data
    ml_prediction = db.Column(db.String(4))  # 'call', 'put', 'none'
    ml_confidence = db.Column(db.Float)
    
    # Market conditions
    volatility = db.Column(db.Float)
    trend_direction = db.Column(db.String(10))  # 'up', 'down', 'sideways'
    
    # Session info
    session_type = db.Column(db.String(10))  # 'morning', 'afternoon', 'manual'
    
    def set_patterns_detected(self, patterns):
        """Set detected patterns as JSON"""
        self.patterns_detected = json.dumps(patterns)
    
    def get_patterns_detected(self):
        """Get detected patterns from JSON"""
        if self.patterns_detected:
            return json.loads(self.patterns_detected)
        return []
    
    def __repr__(self):
        return f'<TradeHistory {self.asset} {self.direction} {self.result}>'

class MLModel(db.Model):
    """Machine Learning model data and performance"""
    __tablename__ = 'ml_models'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Model info
    model_name = db.Column(db.String(50), nullable=False)
    model_type = db.Column(db.String(30))  # 'random_forest', 'gradient_boost', 'svm', 'neural_network'
    asset = db.Column(db.String(20), nullable=False)
    
    # Model parameters (JSON)
    parameters = db.Column(db.Text)  # JSON string of model parameters
    
    # Training data
    training_samples = db.Column(db.Integer, default=0)
    training_start_date = db.Column(db.DateTime)
    training_end_date = db.Column(db.DateTime)
    
    # Performance metrics
    accuracy = db.Column(db.Float)
    precision = db.Column(db.Float)
    recall = db.Column(db.Float)
    f1_score = db.Column(db.Float)
    
    # Live performance
    live_trades = db.Column(db.Integer, default=0)
    live_wins = db.Column(db.Integer, default=0)
    live_accuracy = db.Column(db.Float, default=0.0)
    
    # Model status
    is_active = db.Column(db.Boolean, default=True)
    last_retrained = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_parameters(self, params):
        """Set model parameters as JSON"""
        self.parameters = json.dumps(params)
    
    def get_parameters(self):
        """Get model parameters from JSON"""
        if self.parameters:
            return json.loads(self.parameters)
        return {}
    
    def update_live_performance(self, is_win):
        """Update live performance metrics"""
        self.live_trades += 1
        if is_win:
            self.live_wins += 1
        self.live_accuracy = (self.live_wins / self.live_trades) * 100 if self.live_trades > 0 else 0
    
    def __repr__(self):
        return f'<MLModel {self.model_name} {self.asset} Acc:{self.accuracy}>'

class SystemLog(db.Model):
    """System logs for debugging and monitoring"""
    __tablename__ = 'system_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    level = db.Column(db.String(10))  # 'INFO', 'WARNING', 'ERROR', 'DEBUG'
    component = db.Column(db.String(50))  # 'trading_bot', 'signal_analyzer', 'ml_service', etc.
    message = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Additional context data
    context_data = db.Column(db.Text)  # JSON string for additional context
    
    def set_context_data(self, data):
        """Set context data as JSON"""
        self.context_data = json.dumps(data)
    
    def get_context_data(self):
        """Get context data from JSON"""
        if self.context_data:
            return json.loads(self.context_data)
        return {}
    
    def __repr__(self):
        return f'<SystemLog {self.level} {self.component}>'

class MarketData(db.Model):
    """Market data cache for analysis"""
    __tablename__ = 'market_data'
    
    id = db.Column(db.Integer, primary_key=True)
    asset = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
    # OHLCV data
    open_price = db.Column(db.Float, nullable=False)
    high_price = db.Column(db.Float, nullable=False)
    low_price = db.Column(db.Float, nullable=False)
    close_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Float, default=0)
    
    # Timeframe
    timeframe = db.Column(db.String(5), default='1m')  # '1m', '5m', '15m', '1h', etc.
    
    # Technical indicators (calculated)
    rsi = db.Column(db.Float)
    macd = db.Column(db.Float)
    macd_signal = db.Column(db.Float)
    macd_histogram = db.Column(db.Float)
    ma_20 = db.Column(db.Float)
    ma_50 = db.Column(db.Float)
    aroon_up = db.Column(db.Float)
    aroon_down = db.Column(db.Float)
    
    # Price action analysis
    is_bullish_engulfing = db.Column(db.Boolean, default=False)
    is_bearish_engulfing = db.Column(db.Boolean, default=False)
    is_hammer = db.Column(db.Boolean, default=False)
    is_shooting_star = db.Column(db.Boolean, default=False)
    is_doji = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_asset_timestamp', 'asset', 'timestamp'),
        db.Index('idx_asset_timeframe_timestamp', 'asset', 'timeframe', 'timestamp'),
    )
    
    def __repr__(self):
        return f'<MarketData {self.asset} {self.timestamp} {self.close_price}>'