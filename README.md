# Twitch Smart Home Integration
Permite controlar algumas automações baseadas em eventos no chat da Twitch

# How-to

## Hardware necessário
- Qualquer [lâmpada smart](https://www.amazon.com.br/L%C3%A2mpada-Positivo-Casa-Inteligente-Compat%C3%ADvel/dp/B082FTRR76/ref=sr_1_1?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=lampada+positivo&qid=1615504997&sr=8-1) compatível com Alexa

## Tutorial

### Configuração da Alexa
1. Baixe o aplicativo Amazon Alexa para o seu smartphone
1. Conecte a Alexa com sua conta Amazon
1. Instale sua lâmpada smart e configure-a pelo aplicativo do fabricante
1. Siga as instruções do fabricante da lâmpada para autorizar a Alexa a acessar seus dispositivos

### Configuração do IFTTTrigger
1. Adicione a skill [IFTTTrigger](https://www.amazon.com.br/mkZense-com-LLC-IFTTTrigger/dp/B08M496VGB) em sua conta Amazon
1. Será preciso pagar a versão completa da skill (USD $5/ano)
1. Acessa a página de [webhooks](https://mkzense.com/webhook) e submeta o e-mail usado na sua conta Amazon para receber uma URL com o token dos seus webhooks por email
1. Guarde o token recebido para configuração do script

### Configuração das rotinas
1. Crie as rotinas no aplicativo de celular da Alexa, configurando cada uma das cores desejadas para suas automações:
    1. Use como gatilho (*"quando isso acontecer..."*) os botões virtuais do IFTTTrigger, dentro da opção *"Casa Inteligente"* da Alexa
    1. Use como ações o controle de luzes ou grupos disponíveis na opção *Casa Inteligente*

### Configurando o aplicativo na Twitch
1. Logado em sua conta da Twitch, vá para o [painel de desenvolvedor](https://dev.twitch.tv/console)
1. Registre um novo aplicativo com qualquer nome e categoria, mas adicione obrigatoriamente a seguinte URL de redirecationamento para OAuth: http://localhost:17563
1. Após criar o aplicativo, guarde o ID do cliente fornecido pela Twitch
1. Gere um novo segredo de cliente e guarde junto com a ID do cliente

### Configuração do script
1. Renomeie o arquivo secrets_template.json para secrets.json e mantenha na mesma pasta do script
1. Usando qualquer editor de texto (por ex. o Bloco de Notas) preencha as aspas vazias com os tokens guardados nos passos anteriores
1. Preencha também o nome do seu canal da Twitch, exatamente como exibido, dentro do arquivo secrets.json

### Configuração do ambiente
1. Instale o (Python 3[https://www.python.org/downloads/]) para sua plataforma
1. Durante a instalação, certifique-se de adicionar o Python ao PATH do seu sistema operacional
1. Instale as dependencias do arquivo requirements.txt usando o pip

### Executando e autorizando
1. Execute o script usando: python main.py
1. O script deve ler automaticamente os tokens e te redirecionar para página de autenticação da Twitch
1. Pronto! Seus dispositivos já vão reagir aos eventos de doação de bits e novos subs no seu canal

