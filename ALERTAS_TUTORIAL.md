# 🔔 Sistema de Alertas e Notificações - Central de Licitações

## O que é o Sistema de Alertas?

O sistema de alertas é uma funcionalidade avançada que **monitora automaticamente** todas as licitações publicadas no sistema e avisa quando encontra palavras-chave que você definiu.

### Exemplo de Uso

Você é o gerente de uma empresa chamada "TechSolutions Brasil" com CNPJ "12.345.678/0001-99".

Você adiciona essas palavras-chave:
- ✅ TECHSOLUTIONS BRASIL
- ✅ 12345678000199 (seu CNPJ sem formatação)
- ✅ technology@techsolutions.com.br (seu email)

Quando um pregoeiro publica uma licitação que menciona sua empresa:
- 📋 Licitação #2024.001 - "Contratação de serviços de TI para a Prefeitura"
- 📝 Descrição: "...preferencialmente empresas como TechSolutions Brasil..."

**Resultado:** 🔔 Você recebe AUTOMATICAMENTE um alerta!

---

## ⚙️ Como Configurar Palavras-Chave

### Passo 1: Acessar Configurações
1. No Dashboard, clique em **"⚙️ Configurar Palavras-Chave"**
2. Ou vá a **"🔔 Gerenciar Alertas → ⚙️ Configurar"**

### Passo 2: Adicionar uma Palavra-Chave

**Campos:**
- **Palavra**: A palavra ou expressão a ser monitorada (ex: "TechSolutions Brasil")
- **Tipo**: Selecione qual tipo de identificação
  - Razão Social
  - CNPJ
  - Email
  - Telefone
  - Outro

**Exemplo:**
```
Palavra: ACME LTDA
Tipo: Razão Social
👉 Clique em "+ Adicionar"
```

### Passo 3: Gerenciar Palavras

Na tela de Palavras-Chave você pode:
- ✅ Ver todas as suas palavras monitoradas
- ✅ Visualizar quando foram adicionadas
- 🗑️ Remover uma palavra-chave

---

## 📬 Visualizando Alertas

### Acessar Alertas

1. **Do Dashboard**: Clique no botão **"🔔 Alertas"** no canto superior direito
   - Se tiver alertas não lidos, o número aparece (ex: 🔔 3)
   - Se não tiver, apenas o ícone 🔔

2. **Ou pelo menu**: "🔔 Gerenciar Alertas e Notificações"

### Abas de Alertas

#### 📌 "Não Lidos"
Mostra apenas alertas que você ainda não visualizou.
- Novos alertas aparecem aqui primeiro
- Botão "✓ Marcar como Lido" para confirmar

#### 📋 "Todos"
Mostra todos os alertas (lidos e não lidos)
- Histórico completo de detecções
- Você pode rastrear tudo que foi encontrado

### Informações em Cada Alerta

```
🔍 MENÇÃO - 2024-05-22              [Data do alerta]
├─ Licitação: 2024.001 - Contratação de Serviços
├─ Palavra-chave detectada: TECHSOLUTIONS BRASIL
└─ Mensagem: "A palavra-chave 'TECHSOLUTIONS BRASIL' foi 
   encontrada na licitação 2024.001"
   
[✓ Marcar como Lido]               [Botão de ação]
```

---

## 🎯 Dicas para Melhor Uso

### 1. Use Múltiplas Variações
Se sua empresa tem nomes diferentes, adicione vários:
```
✅ Acme Ltda
✅ ACME LTDA
✅ ACME LTD
✅ 12345678000199  (CNPJ)
```

### 2. Adicione Identificadores
Além da razão social, monitore:
```
✅ Seu CNPJ (com ou sem formatação)
✅ Email corporativo
✅ Telefone principal
✅ Nomes de sócios/diretores
✅ Sigla ou apelido da empresa
```

### 3. Verifique Regularmente
- 📲 Clique na aba "Alertas" do Dashboard frequentemente
- 🔔 Veja o contador no botão de alertas
- ✓ Marque como lidos para organizar

### 4. Organize seus Alertas
```
Leitura rápida:
1. Abra "Não Lidos"
2. Analise cada alerta
3. Clique "Marcar como Lido"
4. Acesse a licitação se interessado
```

---

## 🔍 Como Funciona Internamente

### Processo de Detecção

```
1. Usuário cria uma licitação
        ↓
2. Sistema busca TODAS as palavras-chave de TODOS os usuários
        ↓
3. Compara com: número, título, descrição e órgão da licitação
        ↓
4. Se encontrar correspondência:
        ↓
5. Cria um ALERTA para o usuário
        ↓
6. Usuário recebe notificação (🔔)
```

### O que é Monitorado?

Quando você adiciona uma palavra-chave, o sistema busca em:
- ✅ **Número** da licitação (ex: "2024.001.001")
- ✅ **Título** (ex: "Contratação de Serviços...")
- ✅ **Descrição** (conteúdo detalhado)
- ✅ **Órgão** (ex: "Prefeitura de São Paulo")

### Sensibilidade à Case (Maiúscula/Minúscula)

⚠️ **Importante:** O sistema **NÃO diferencia** maiúsculas de minúsculas

```
Você adiciona:     techsolutions brasil
Sistema detecta:   TECHSOLUTIONS BRASIL ✅
                   TechSolutions Brasil ✅
                   techsolutions brasil ✅
```

---

## 📊 Estatísticas de Alertas

Quando você marca alertas como lidos e gerencia suas palavras-chave, o sistema mantém:

- 📈 Total de alertas gerados
- 📖 Alertas lidos vs. não lidos
- 🏷️ Alertas por tipo (menção, notificação, etc.)
- 📅 Histórico completo com datas

---

## ⚡ Casos de Uso Comuns

### 1. Empresa Participando de Licitações
```
Adicione:
- Razão Social: "Minha Empresa LTDA"
- CNPJ: "12345678000199"
- Email: "contato@minha-empresa.com.br"

Resultado: Fica atento a TODAS as licitações que a mencionam
```

### 2. Representante de Consórcio
```
Adicione:
- Todas as empresas do consórcio
- Emails de contato
- CNPJs

Resultado: Monitora licitações para o consórcio inteiro
```

### 3. Pesquisador/Analista
```
Adicione:
- Órgãos governamentais de interesse
- Setores específicos (tecnologia, saúde, etc.)
- Termos técnicos

Resultado: Acompanha tendências de licitações
```

### 4. Contador/Consultor
```
Adicione:
- Nomes de clientes
- CNPJs de clientes
- Ramos de atividade

Resultado: Monitora oportunidades para seus clientes
```

---

## ❓ Dúvidas Frequentes

**P: Quanto tempo leva para o alerta aparecer?**
R: Instantaneamente! Quando uma licitação é criada, o alerta é gerado imediatamente.

**P: Posso ter muitas palavras-chave?**
R: Sim! Não há limite. Quanto mais específicas, melhores os resultados.

**P: Como removo uma palavra-chave?**
R: Vá em "⚙️ Configurar Palavras-Chave", encontre a palavra e clique em "🗑️ Remover".

**P: Qual é a diferença entre "Não Lidos" e "Todos"?**
R: "Não Lidos" = novos alertas / "Todos" = histórico completo

**P: Posso editar uma palavra-chave?**
R: Atualmente não. Remova e adicione novamente com a variação desejada.

**P: Se eu deletar uma palavra-chave, os alertas antigos desaparecem?**
R: Não. Os alertas já criados continuam no histórico, apenas novos alertas deixarão de ser gerados.

---

## 🚀 Próximos Passos

Depois de configurar suas palavras-chave:

1. ✅ Revise o Dashboard - veja os alertas não lidos
2. ✅ Explore Licitações - acesse as que mencionam sua empresa
3. ✅ Ajuste Palavras-Chave - refine baseado nos resultados
4. ✅ Mantenha Atualizado - revise periodicamente

---

**Versão**: 1.0  
**Última atualização**: 22 de maio de 2024  
**Sistema**: Central de Licitações - Módulo de Alertas e Notificações
