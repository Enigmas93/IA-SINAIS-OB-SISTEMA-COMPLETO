# IA Sinais OB - Sistema Inteligente de Trading

🤖 Sistema automatizado de trading para IQ Option com análise técnica avançada, Machine Learning e interface web moderna.

## 📋 Funcionalidades

### 🎯 Core Features
- **Análise de Gráfico em Tempo Real**: Captura de candles e análise via Price Action + indicadores técnicos
- **Configurações Dinâmicas**: Interface para definir horários, ativos, take profit, stop loss, martingale
- **Loop de Execução**: Robô funciona em loop contínuo com pausa automática ao atingir metas
- **Painel Web**: Histórico filtrável, estatísticas detalhadas, gráficos de evolução
- **Execução Automática**: Entrada automática na IQ Option baseada em sinais detectados

### 🧠 Inteligência Artificial
- **Machine Learning**: Modelos Random Forest, Gradient Boosting, SVM e Neural Networks
- **Otimização de Sinais**: Aprendizado contínuo baseado em resultados históricos
- **Análise Preditiva**: Refinamento automático dos modelos com base nas operações

### 📊 Análise Técnica
- **Price Action**: Padrões como Engolfo, Martelo, Shooting Star, Doji, Morning/Evening Star
- **Indicadores**: RSI, MACD, Aroon, Médias Móveis, Bollinger Bands, Stochastic, ATR
- **Sistema de Martingale**: Até 3 níveis com controle inteligente de loss

### 🔐 Segurança
- **Autenticação JWT**: Sistema seguro de login e sessões
- **Criptografia**: Senhas e dados sensíveis protegidos
- **Multiusuário**: Cada usuário vê apenas seus dados e configurações

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Flask**: Framework web
- **SQLAlchemy**: ORM para banco de dados
- **Flask-JWT-Extended**: Autenticação JWT
- **IQ Option API**: Integração com a corretora
- **Scikit-learn**: Machine Learning
- **TA-Lib**: Análise técnica
- **APScheduler**: Agendamento de tarefas

### Frontend
- **HTML5, CSS3, JavaScript**
- **Bootstrap 5**: Framework CSS
- **Chart.js**: Gráficos interativos
- **Font Awesome**: Ícones

### Banco de Dados
- **SQLite** (desenvolvimento)
- **PostgreSQL** (produção)

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

### 1. Clone o Repositório
```bash
git clone <repository-url>
cd IA-SINAIS-OB
```

### 2. Crie um Ambiente Virtual
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente
Crie um arquivo `.env` baseado no `.env.example`:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta_muito_segura_aqui
FLASK_APP=app.py

# Database
DATABASE_URL=sqlite:///trading_bot.db

# JWT Configuration
JWT_SECRET_KEY=sua_jwt_secret_key_aqui
JWT_ACCESS_TOKEN_EXPIRES=604800

# Trading Configuration
DEFAULT_TRADE_AMOUNT=10.0
DEFAULT_MARTINGALE_LEVELS=3
DEFAULT_TAKE_PROFIT=70.0
DEFAULT_STOP_LOSS=30.0

# Security
RATE_LIMIT_PER_MINUTE=60
MAX_LOGIN_ATTEMPTS=5

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/trading_bot.log
```

### 5. Inicialize o Banco de Dados
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 6. Execute a Aplicação
```bash
python app.py
```

A aplicação estará disponível em: `http://localhost:5000`

## 🌐 Deploy na Render.com

### 1. Prepare o Repositório
Certifique-se de que os arquivos `render.yaml`, `Procfile` e `requirements.txt` estão no repositório.

### 2. Conecte ao GitHub
1. Faça push do código para um repositório GitHub
2. Acesse [Render.com](https://render.com)
3. Conecte sua conta GitHub

### 3. Configure o Serviço
1. Clique em "New" → "Web Service"
2. Selecione seu repositório
3. Configure:
   - **Name**: `ia-sinais-ob`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

### 4. Configure Variáveis de Ambiente
Adicione as seguintes variáveis no painel da Render:

```
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta_de_producao
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=sua_jwt_secret_de_producao
```

### 5. Configure o Banco de Dados
1. Crie um PostgreSQL database na Render
2. Copie a URL de conexão
3. Adicione como `DATABASE_URL` nas variáveis de ambiente

## 📖 Como Usar

### 1. Primeiro Acesso
1. Acesse a aplicação
2. Clique em "Cadastre-se aqui"
3. Preencha seus dados e credenciais da IQ Option
4. Faça login com suas credenciais

### 2. Configuração Inicial
1. No dashboard, clique em "Configurações"
2. Configure:
   - **Ativo**: Par de moedas para operar
   - **Valor por Entrada**: Valor fixo ou % do saldo
   - **Take Profit/Stop Loss**: Metas de lucro e perda
   - **Martingale**: Níveis de recuperação
   - **Horários**: Sessões manhã e tarde
   - **Modo**: Automático ou Manual

### 3. Operação Manual
1. Configure o bot
2. Clique em "Iniciar Bot"
3. O sistema operará até atingir as metas
4. Clique em "Parar Bot" quando necessário

### 4. Operação Automática
1. Configure o modo "Automático"
2. Defina os horários de operação
3. O bot iniciará automaticamente nos horários definidos
4. Pausará ao atingir take profit ou stop loss

### 5. Monitoramento
- **Dashboard**: Visão geral em tempo real
- **Histórico**: Filtros por data, resultado, ativo
- **Estatísticas**: Win rate, lucro total, sequências
- **Gráficos**: Evolução do lucro ao longo do tempo

## 🔧 Configurações Avançadas

### Machine Learning
O sistema treina automaticamente modelos ML baseados no histórico de trades:

- **Random Forest**: Análise de padrões complexos
- **Gradient Boosting**: Otimização sequencial
- **SVM**: Classificação de sinais
- **Neural Networks**: Aprendizado profundo

### Análise Técnica
Indicadores configuráveis:

```python
# Exemplo de configuração de indicadores
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BB_PERIOD = 20
BB_STD = 2
```

### Price Action
Padrões detectados automaticamente:

- **Engolfo de Alta/Baixa**
- **Martelo/Shooting Star**
- **Doji**
- **Morning Star/Evening Star**
- **Hammer/Inverted Hammer**

## 📊 API Endpoints

### Autenticação
- `POST /api/auth/register` - Cadastro
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout

### Configuração
- `GET /api/config` - Obter configuração
- `POST /api/config` - Salvar configuração

### Bot
- `POST /api/bot/start` - Iniciar bot
- `POST /api/bot/stop` - Parar bot
- `GET /api/bot/status` - Status do bot

### Dashboard
- `GET /api/dashboard/stats` - Estatísticas
- `GET /api/trades/history` - Histórico de trades

## 🐛 Troubleshooting

### Problemas Comuns

**1. Erro de conexão com IQ Option**
```
Solução: Verifique credenciais e conexão com internet
```

**2. Bot não inicia**
```
Solução: Verifique configurações e logs do sistema
```

**3. Erro de banco de dados**
```
Solução: Recrie o banco com: python -c "from app import db; db.create_all()"
```

### Logs
Verifique os logs em:
- Desenvolvimento: Console do terminal
- Produção: `logs/trading_bot.log`

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## ⚠️ Disclaimer

**AVISO IMPORTANTE**: Este software é fornecido apenas para fins educacionais e de pesquisa. O trading de opções binárias envolve riscos significativos e pode resultar na perda total do capital investido. 

- Use apenas em conta demo inicialmente
- Nunca invista mais do que pode perder
- O desempenho passado não garante resultados futuros
- Os desenvolvedores não se responsabilizam por perdas financeiras

## 📞 Suporte

Para suporte e dúvidas:
- Abra uma issue no GitHub
- Consulte a documentação
- Verifique os logs de erro

---

**Desenvolvido com ❤️ para a comunidade de trading**