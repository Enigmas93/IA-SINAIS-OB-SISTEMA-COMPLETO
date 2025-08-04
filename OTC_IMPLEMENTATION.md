# Implementação de Ativos OTC (Over-The-Counter)

## Resumo das Implementações

Foi implementado suporte completo aos ativos OTC no sistema de trading bot da IQ Option. Os OTCs são ativos que ficam disponíveis 24 horas por dia, 7 dias por semana, diferentemente dos ativos regulares que seguem horários específicos de mercado.

## Ativos Implementados

### Forex - Mercado Regular
- EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD
- EUR/GBP, EUR/JPY, GBP/JPY, USD/CHF, AUD/CAD
- AUD/JPY, CAD/JPY, CHF/JPY, EUR/AUD, EUR/CAD
- EUR/CHF, GBP/AUD, GBP/CAD, GBP/CHF, NZD/USD
- NZD/CAD, NZD/CHF, NZD/JPY, AUD/CHF, AUD/NZD
- CAD/CHF

### OTC - Over The Counter (24h)
- EUR/USD OTC, GBP/USD OTC, USD/JPY OTC, AUD/USD OTC, USD/CAD OTC
- EUR/GBP OTC, EUR/JPY OTC, GBP/JPY OTC, USD/CHF OTC, AUD/CAD OTC
- AUD/JPY OTC, CAD/JPY OTC, CHF/JPY OTC, EUR/AUD OTC, EUR/CAD OTC
- EUR/CHF OTC, GBP/AUD OTC, GBP/CAD OTC, GBP/CHF OTC, NZD/USD OTC
- NZD/CAD OTC, NZD/CHF OTC, NZD/JPY OTC, AUD/CHF OTC, AUD/NZD OTC
- CAD/CHF OTC

## Melhorias Implementadas

### 1. Interface do Usuário (base.html)
- Adicionados grupos organizados de ativos (Forex Regular e OTC)
- Interface mais clara com separação visual entre tipos de ativos
- Todos os principais pares de moedas disponíveis

### 2. Serviço IQ Option (iq_option_service.py)
- **get_available_assets()**: Melhorado com logs detalhados
- **is_asset_open()**: Implementação inteligente que:
  - Verifica status do ativo solicitado
  - Automaticamente tenta versão OTC se o regular estiver fechado
  - Logs detalhados para debugging
  - Suporte a diferentes estruturas de resposta da API
- **get_candles()**: Implementação robusta que:
  - Tenta obter candles do ativo solicitado
  - Automaticamente tenta versão OTC se falhar
  - Logs detalhados do processo
  - Melhor tratamento de timeframes

### 3. Trading Bot (trading_bot.py)
- **Verificação inteligente de ativos**: Automaticamente muda para OTC quando necessário
- **Execução de trades**: Usa versão OTC quando o ativo regular não está disponível
- **Logs melhorados**: Informa quando está usando versão OTC
- **Fallback automático**: Sistema nunca para por ativo indisponível

## Como Funciona

### Verificação Automática de Ativos
1. Sistema verifica se o ativo selecionado está aberto
2. Se fechado, automaticamente verifica versão OTC
3. Se OTC disponível, usa automaticamente
4. Logs informam qual versão está sendo usada

### Obtenção de Candles
1. Tenta obter dados do ativo selecionado
2. Se falhar, automaticamente tenta versão OTC
3. Retorna dados da versão disponível
4. Logs detalham o processo

### Execução de Trades
1. Verifica disponibilidade antes de cada trade
2. Usa versão OTC se necessário
3. Registra qual ativo foi realmente usado
4. Mantém histórico correto

## Vantagens dos OTCs

1. **Disponibilidade 24/7**: Negociação contínua
2. **Menor volatilidade**: Movimentos mais suaves
3. **Backup automático**: Sistema nunca para por mercado fechado
4. **Flexibilidade**: Mais opções de trading

## Logs e Debugging

O sistema agora fornece logs detalhados:
- Status de cada ativo verificado
- Quando muda para versão OTC
- Quantidade de candles obtidos
- Qual ativo está sendo usado para trades

## Uso Prático

1. **Selecione qualquer ativo** na interface
2. **Sistema automaticamente** verifica disponibilidade
3. **Usa versão OTC** se necessário
4. **Trading contínuo** sem interrupções

## Compatibilidade

Todas as implementações são:
- **Retrocompatíveis**: Funciona com código existente
- **Automáticas**: Não requer configuração adicional
- **Transparentes**: Usuário não precisa se preocupar com detalhes
- **Robustas**: Tratamento completo de erros

O sistema agora está completamente preparado para trading 24/7 com suporte automático aos ativos OTC da IQ Option.