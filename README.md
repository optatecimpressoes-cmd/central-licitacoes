# Central de Licitações

Uma aplicação desktop completa para gerenciamento e visualização de licitações públicas, desenvolvida em Python com CustomTkinter.

## 🎯 Funcionalidades

- ✅ **Autenticação**: Sistema de login e registro de usuários
- ✅ **Dashboard**: Visualização de estatísticas gerais (total de licitações, valores, etc.)
- ✅ **CRUD de Licitações**: Criar, ler, atualizar e deletar licitações
- ✅ **Busca e Filtros**: Filtrar licitações por título, número ou órgão
- ✅ **Exportação**: Exportar licitações em Excel e PDF
- ✅ **Banco de Dados**: SQLite integrado para persistência de dados
- ✅ **Interface Moderna**: UI responsiva com CustomTkinter

## 📋 Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## 🚀 Instalação e Execução

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a Aplicação

```bash
python app.py
```

## 📖 Como Usar

### Primeira Vez

1. **Registrar uma conta**: Na tela de login, clique em "Registrar"
2. **Preencher os dados**: Nome, email, usuário e senha
3. **Fazer login**: Use as credenciais criadas

### Criar uma Licitação

1. No Dashboard, clique em "+ Nova Licitação"
2. Preencha os campos obrigatórios:
   - Número da Licitação
   - Título
   - Órgão
   - Modalidade (Pregão, Concorrência, etc.)
   - Datas de abertura e encerramento
   - Valor estimado
3. Clique em "Salvar"

### Buscar e Filtrar

1. Acesse "Listar Licitações"
2. Use a barra de filtro para buscar por:
   - Título
   - Número
   - Órgão
3. Clique em "Filtrar"

### Exportar Dados

1. Na listagem de licitações, os dados podem ser exportados (funcionalidade em desenvolvimento)
2. Acesse o menu "Relatórios" para exportar em PDF ou Excel

## 📁 Estrutura do Projeto

```
CentralLicitacoes/
├── app.py                 # Aplicação principal
├── config.py             # Configurações gerais
├── database.py           # Gerenciamento do banco de dados
├── requirements.txt      # Dependências Python
├── ui/                   # Interface do usuário
│   ├── __init__.py
│   ├── login_frame.py   # Tela de login e registro
│   ├── dashboard_frame.py # Dashboard principal
│   └── licitacao_frame.py # Telas de licitações
├── services/             # Serviços da aplicação
│   ├── __init__.py
│   └── export_service.py # Serviço de exportação
├── data/                 # Banco de dados (criado automaticamente)
└── reports/              # Relatórios exportados
```

## 🔒 Segurança

- Senhas são hasheadas com SHA-256
- Validação de entrada em todos os formulários
- Isolamento de dados por usuário

## 📊 Banco de Dados

A aplicação usa SQLite com as seguintes tabelas:

- **usuarios**: Armazena informações de login
- **licitacoes**: Armazena licitações cadastradas
- **documentos**: Armazena referências de documentos (expansão futura)

## 🔧 Configurações

Edite `config.py` para personalizar:

- Dimensões da janela
- Tema de cores
- Caminho do banco de dados
- Diretórios de saída

## 🚧 Roadmap

- [ ] Upload de documentos
- [ ] Notificações de alterações
- [ ] Usuários com diferentes permissões (Admin, Visualizador, etc.)
- [ ] Sincronização com APIs governamentais
- [ ] Gráficos avançados e relatórios
- [ ] Suporte a múltiplos idiomas

## 📝 Notas

- Os dados são salvos em `data/central_licitacoes.db`
- Relatórios exportados são salvos em `reports/`
- A aplicação cria automaticamente os diretórios necessários

## 💡 Dicas

- Use números descritivos para as licitações (ex: "2024.001.001")
- Mantenha os valores em reais sem R$
- Datas no formato YYYY-MM-DD (2024-05-22)

## 📞 Suporte

Para dúvidas ou problemas, verifique:
1. Se todas as dependências estão instaladas
2. Se Python 3.8+ está instalado
3. Permissões de escrita no diretório da aplicação

---

**Versão**: 1.0.0 MVP  
**Última atualização**: 22 de maio de 2024
