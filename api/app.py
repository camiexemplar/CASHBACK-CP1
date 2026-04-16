import os
from flask import Flask, request, render_template_string
import oracledb

app = Flask(__name__)

# ================= DB (VERCEL ENV SAFE) =================
DB_CONFIG = {
    "user": os.getenv("DB_USER", "RM566520"),
    "password": os.getenv("DB_PASSWORD", "856932"),
    "dsn": os.getenv("DB_DSN", "oracle.fiap.com.br:1521/ORCL")
}

# ================= SEU HTML (INTACTO) =================
HTML = """<!DOCTYPE html>
<html lang="pt-br">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Eco-Awareness 2026</title>

<style>
:root {
    --bg-color: #0d1117;
    --card-bg: #161b22;
    --primary-green: #00ff88;
    --text-gray: #8b949e;
    --border-color: #30363d;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    background-color: var(--bg-color);
    color: #c9d1d9;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 40px 0;
}

.container {
    background-color: var(--card-bg);
    width: 90%;
    max-width: 650px;
    padding: 40px;
    border-radius: 20px;
    border: 1px solid var(--border-color);
    text-align: center;
}

.badge {
    background-color: #00ff8822;
    color: var(--primary-green);
    font-weight: bold;
    font-size: 11px;
    padding: 4px 12px;
    border-radius: 50px;
    text-transform: uppercase;
    border: 1px solid var(--primary-green);
    display: inline-block;
    margin-bottom: 15px;
}

h1 { font-size: 28px; margin: 0; color: white; }
h2 { font-size: 18px; color: var(--primary-green); margin-top: 40px; text-align: left; border-bottom: 1px solid var(--border-color); padding-bottom: 10px;}
.subtitle { color: var(--text-gray); font-size: 14px; margin-bottom: 30px; }

.context-box {
    background: #00ff8805;
    border-left: 3px solid var(--primary-green);
    padding: 20px;
    text-align: left;
    margin-bottom: 25px;
    border-radius: 0 10px 10px 0;
}

.context-box h3 { color: var(--primary-green); font-size: 16px; margin-top: 0; }
.context-box p { font-size: 13px; line-height: 1.5; color: #8b949e; margin-bottom: 0; }

.rules { text-align: left; margin-bottom: 25px; }
.rules h4 { color: var(--primary-green); font-size: 14px; margin-bottom: 10px; }
.rules ul { list-style: none; padding: 0; margin: 0; }
.rules li { font-size: 13px; margin-bottom: 6px; color: #8b949e; }
.rules li::before { content: "• "; color: var(--primary-green); }

.input-group { text-align: left; margin-bottom: 20px; }
label { display: block; font-size: 11px; color: var(--text-gray); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }

input[type="text"] {
    width: 100%;
    background: #0d1117;
    border: 1px solid var(--border-color);
    padding: 12px;
    border-radius: 8px;
    color: white;
    box-sizing: border-box;
}

.btn-submit {
    width: 100%;
    background-color: var(--primary-green);
    color: #0d1117;
    border: none;
    padding: 15px;
    border-radius: 10px;
    font-weight: bold;
    font-size: 14px;
    cursor: pointer;
    text-transform: uppercase;
    transition: 0.2s;
}

.btn-submit:hover { opacity: 0.9; transform: translateY(-1px); }

.log-msg { margin-top: 20px; font-size: 13px; color: var(--primary-green); }

table { width: 100%; margin-top: 20px; border-collapse: collapse; font-size: 12px; text-align: left; }
th { color: var(--primary-green); border-bottom: 1px solid var(--border-color); padding: 10px 5px; }
td { padding: 10px 5px; border-bottom: 1px solid #21262d; }

.footer-link { display: block; margin-top: 25px; color: var(--text-gray); text-decoration: none; font-size: 12px; }
</style>
</head>

<body>

<div class="container">

<div class="badge">Fidelidade & Bônus</div>
<h1>Eco-Awareness 2026</h1>
<p class="subtitle">Programa de Cashback Progressivo</p>

<div class="context-box">
<h3>Contexto do Desafio (Estória)</h3>
<p>"Como analista financeiro de engajamento do Eco-Awareness..."<br><br>
Sustentabilidade requer recompensas a longo prazo.</p>
</div>

<div class="rules">
<h4>Regras de Negócio</h4>
<ul>
<li>Cursor Explícito</li>
<li>Contagem de presenças</li>
<li>Cashback progressivo</li>
</ul>
</div>

<form method="POST">
<div class="input-group">
<label>ID do Evento Finalizado</label>
<input type="text" name="evento_id" required>
</div>
<button class="btn-submit" type="submit">Distribuir Créditos</button>
</form>

{% if mensagem %}
<div class="log-msg">{{mensagem}}</div>
{% endif %}

<h2>Dashboard</h2>
<table>
<thead>
<tr>
<th>Usuário</th>
<th>Saldo</th>
<th>Presenças</th>
<th>Tipo</th>
</tr>
</thead>
<tbody>
{% for u in usuarios %}
<tr>
<td>{{u[0]}}</td>
<td>R$ {{u[2]}}</td>
<td>{{u[5]}}</td>
<td>{{u[3]}}</td>
</tr>
{% endfor %}
</tbody>
</table>

<h2>Log de Auditoria</h2>
<table>
<tbody>
{% for l in auditoria %}
<tr>
<td>#{{l[0]}}</td>
<td>#{{l[1]}}</td>
<td>{{l[2]}}</td>
<td>{{l[3]}}</td>
</tr>
{% endfor %}
</tbody>
</table>

</div>

</body>
</html>
"""

# ================= PL/SQL =================
PLSQL_BLOCK = """
DECLARE
    CURSOR c_participantes IS
        SELECT i.id, i.usuario_id, i.valor_pago, i.tipo
        FROM INSCRICOES i
        WHERE i.status = 'PRESENT'
        AND i.evento_id = :evento_id;

    v_presencas NUMBER;
    v_cashback NUMBER;
    v_percentual NUMBER;
BEGIN
    FOR participante IN c_participantes LOOP

        SELECT COUNT(*) INTO v_presencas
        FROM INSCRICOES
        WHERE usuario_id = participante.usuario_id
        AND status = 'PRESENT';

        IF v_presencas > 3 THEN
            v_percentual := 0.25;
        ELSIF participante.tipo = 'VIP' THEN
            v_percentual := 0.20;
        ELSE
            v_percentual := 0.10;
        END IF;

        v_cashback := participante.valor_pago * v_percentual;

        UPDATE USUARIOS
        SET saldo = saldo + v_cashback
        WHERE id = participante.usuario_id;

        INSERT INTO LOG_AUDITORIA (id, inscricao_id, motivo, data)
        VALUES (LOG_AUDITORIA_SEQ.NEXTVAL, participante.id, 'Cashback', SYSDATE);

    END LOOP;

    COMMIT;
END;
"""

# ================= ROUTE =================
@app.route("/", methods=["GET", "POST"])
def index():

    mensagem = None
    usuarios = []
    auditoria = []

    conn = None

    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # EXEC PL/SQL
        if request.method == "POST":
            evento_id = request.form.get("evento_id")
            if evento_id:
                cursor.execute(PLSQL_BLOCK, evento_id=evento_id)
                mensagem = "Cashback distribuído com sucesso!"

        # USERS
        cursor.execute("""
            SELECT u.nome, u.email, u.saldo,
                   NVL(MAX(i.tipo),'NORMAL'),
                   COUNT(i.id),
                   COUNT(i.id)
            FROM USUARIOS u
            LEFT JOIN INSCRICOES i ON u.id = i.usuario_id
            GROUP BY u.nome,u.email,u.saldo
        """)
        usuarios = cursor.fetchall()

        # AUDIT
        cursor.execute("""
            SELECT id, inscricao_id, motivo,
                   TO_CHAR(data,'DD/MM HH24:MI')
            FROM LOG_AUDITORIA
            ORDER BY data DESC
            FETCH FIRST 10 ROWS ONLY
        """)
        auditoria = cursor.fetchall()

    except Exception as e:
        mensagem = str(e)

    finally:
        if conn:
            conn.close()

    return render_template_string(HTML,
                                  mensagem=mensagem,
                                  usuarios=usuarios,
                                  auditoria=auditoria)