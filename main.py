import tweepy # biblioteca para trabalhar com o twitter
import pandas as pd
from textblob import TextBlob # Trabalha com analise de sentimentos
from datetime import datetime

# Configurando as chaves de acesso

# Dados das chaves
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# AUTENTICANDO

# realizando a autenticação
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=5, retry_delay=10)

count = 50 # total de registros que queremos recuperar
lang = '' # Idioma que a gente ta querendo pegar
keyword = "''" # Palavra que vai ser procurada

# Configurar a requisicao ao twitter 
tweets = api.search(
    q=keyword, # Palavra ou frase para pesquisa
    rpp = count, # Numero de registro a serem retornados
    result_type = 'mixed', # Tipo de resultado que queremos (Texto completo da mensagem)
    since = datetime(2020, 6, 30, 0, 0, 0).date(), # data a partir da qual queremos pesquisar
    lang = lang, # Idioma da pesquisa
    
)


dados = [] # Vamos guardar os dados de retorno
sentimento = [] # Vamos guardar o sentimento de cada frase (postagem)


for tweet in tweets: # Percorrer cada uma das mensagens retornadas
  frase = TextBlob(tweet.text) # Colocamos cada mensagem retornada da variavel para tratamento

  # Vamos traduzir automaticamente para o ingles, a fim de usar a biblioteca TextBlob para verificar o sentimento
  if frase.detect_language() != 'en':
    traducao = TextBlob(str(frase.translate(to='en')))
    dados.append([tweet.user.name, tweet.text, traducao.sentiment[0], traducao.sentiment[1]])
  else:
    dados.append([tweet.user.name, tweet.text, frase.sentiment[0], frase.sentiment[1]])


  # Verificar os sentimentos
  if traducao.sentiment[0] > 0:
    sentimento.append('Positivo')
  elif traducao.sentiment[0] < 0:
    sentimento.append('Negativo')
  else:
    sentimento.append('Indiferente/Neutro')


