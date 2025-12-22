# 🔗 LinkManager - Gerenciador de Links Inteligente

> Um sistema Full Stack para gerenciamento, categorização e compartilhamento de links, com analytics de cliques e perfis públicos.

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?style=for-the-badge&logo=flask)
![Status](https://img.shields.io/badge/Status-Finalizado-success?style=for-the-badge)

## 🖥️ Sobre o Projeto
O **LinkManager** não é apenas um bloco de notas para URLs. É uma aplicação completa que permite aos usuários criar um repositório pessoal de links úteis, organizá-los visualmente por categorias e compartilhar uma página pública (estilo Linktree) com o mundo.

O sistema conta com **Analytics de Cliques**, permitindo monitorar o engajamento de cada link compartilhado.

## ✨ Funcionalidades Principais

* **🔐 Autenticação Segura:** Sistema de Login/Logout com hash de senhas.
* **🎨 Temas Dinâmicos:** Interface moderna com **Glassmorphism** e alternância entre Modo Claro e Modo Escuro (Tokito Theme).
* **📂 Organização Visual:** Categorias coloridas (Estudos, Trabalho, Animes) para rápida identificação.
* **🔍 Busca Instantânea:** Filtragem em tempo real (JavaScript) por nome ou categoria.
* **📈 Analytics:** Contador de cliques integrado com redirecionamento inteligente.
* **🌍 Perfil Público:** Página de portfólio acessível externamente (ex: /u/yago) que exibe apenas links marcados como públicos.
* **📸 Perfil Personalizável:** Upload de foto de perfil com armazenamento local.

## 🛠️ Tecnologias Utilizadas

* **Back-end:** Python, Flask, Werkzeug.
* **Banco de Dados:** SQLite (SQLAlchemy ORM).
* **Front-end:** HTML5, CSS3 (Variáveis CSS, Flexbox/Grid), JavaScript Puro.
* **Template Engine:** Jinja2.

## 🚀 Como Rodar Localmente

1.  **Clone o repositório:**
    \`\`\`bash
    git clone https://github.com/SEU-USUARIO/LinkManager.git
    cd LinkManager
    \`\`\`

2.  **Instale as dependências:**
    \`\`\`bash
    pip install -r requirements.txt
    \`\`\`

3.  **Execute a aplicação:**
    \`\`\`bash
    python app.py
    \`\`\`
4.  Acesse http://127.0.0.1:5000 no seu navegador.

---
Desenvolvido por **Yago Costa** 🚀