from flask import Flask, render_template, request, Response, url_for
from weasyprint import HTML
from io import BytesIO

app = Flask(__name__)

pecados = {
    "1. Amar a Deus sobre todas as coisas": [
        "Negligência na oração diária",
        "Dúvidas sobre a fé e críticas aos ensinamentos da Igreja",
        "Desânimo espiritual e revolta contra Deus",
        "Frequentar cultos ou práticas supersticiosas (ex: cartomantes, horóscopos)",
        "Buscar glória pessoal acima da vontade de Deus",
        "Orgulho, vaidade ou apego a elogios",
        "Apego excessivo ao dinheiro e aos bens materiais"
    ],
    "2. Não tomar o nome de Deus em vão": [
        "Usar o nome de Deus ou dos santos de forma desrespeitosa",
        "Ridicularizar símbolos da fé ou religiosos",
        "Fazer promessas sem intenção de cumprir",
        "Juramentos falsos ou desnecessários",
        "Permitir ou rir quando outros zombam da fé"
    ],
    "3. Guardar domingos e festas de guarda": [
        "Faltar à missa dominical ou em dias santos sem necessidade grave",
        "Chegar intencionalmente atrasado à missa ou sair antes da bênção final",
        "Comungar em pecado mortal",
        "Deixar de se confessar ao menos uma vez ao ano",
        "Não jejuar ou não fazer abstinência quando mandado pela Igreja",
        "Negligenciar a ajuda material à Igreja"
    ],
    "4. Honrar pai e mãe": [
        "Desobediência e falta de respeito aos pais ou superiores",
        "Negligência nos cuidados com os pais idosos ou doentes",
        "Maltrato ao cônjuge em palavras ou atitudes",
        "Dar mau exemplo aos filhos",
        "Permitir influência negativa sobre os filhos (TV, internet, amizades)",
        "Negligência na formação religiosa dos filhos",
        "Deixar de corrigir os filhos por comodismo"
    ],
    "5. Não matar": [
        "Ódio, rancor, inimizade ou desejo de vingança",
        "Falta de perdão",
        "Desejar a morte ou o mal a alguém (ou a si mesmo)",
        "Aborto, eutanásia ou apoio a essas práticas",
        "Descuido com a saúde (excesso de comida, drogas, bebida, sedentarismo)",
        "Riscos desnecessários à vida (direção imprudente, vícios)",
        "Dar escândalo ou mau exemplo"
    ],
    "6. Não pecar contra a castidade": [
        "Pensamentos ou desejos impuros voluntários",
        "Masturbação, pornografia, sexo fora do casamento",
        "Infidelidade emocional ou física",
        "Liberdades excessivas no namoro",
        "Usar roupas provocativas com intenção",
        "Conversas ou piadas imorais",
        "Consumir conteúdo sexualizado (TV, filmes, redes sociais)",
        "Amizades que me levam ao pecado"
    ],
    "7. Não roubar": [
        "Furto, desonestidade em contratos ou negócios",
        "Apropriar-se de bens ou dinheiro indevidamente",
        "Não pagar dívidas justas ou salários devidos",
        "Desperdiçar o tempo no trabalho ou trabalhar com negligência",
        "Vício em jogos de azar",
        "Viver acima dos próprios meios"
    ],
    "8. Não levantar falso testemunho": [
        "Mentira habitual, mesmo sem prejudicar diretamente",
        "Calúnia, difamação ou exagerar defeitos dos outros",
        "Ouvir ou espalhar boatos",
        "Julgar mal ou condenar injustamente alguém",
        "Causar divisão entre pessoas por fofoca",
        "Não reparar a má reputação causada por mim"
    ],
    "9. Não desejar a mulher do próximo": [
        "Desejos impuros por pessoa casada ou consagrada",
        "Fantasias ou intenções de infidelidade",
        "Assédio verbal ou físico",
        "Flertes com pessoas comprometidas",
        "Curiosidade indevida sobre a intimidade alheia"
    ],
    "10. Não cobiçar as coisas alheias": [
        "Invejar os bens, sucesso ou talentos dos outros",
        "Desejo de tomar ou imitar o que pertence a outro",
        "Descontentamento com a própria vida por comparação"
    ],
    "Mandamentos da Igreja": [
        "Faltar à Missa em festas de guarda",
        "Não confessar-se ao menos uma vez por ano",
        "Não comungar na Páscoa",
        "Comungar em pecado grave",
        "Não guardar jejum e abstinência nos tempos prescritos",
        "Não ajudar a Igreja materialmente"
    ],
    "Pecados relacionados ao casamento e à família": [
        "Negligência com o cônjuge (diálogo, carinho, atenção)",
        "Violência física ou verbal dentro do lar",
        "Desrespeito mútuo entre os cônjuges",
        "Falta de perdão no matrimônio",
        "Priorizar trabalho ou lazer em detrimento da família",
        "Não se abrir à vida (rejeitar filhos sem justa causa)",
        "Não dar testemunho cristão dentro do lar"
    ],
    "Pecados espirituais e morais": [
        "Preguiça espiritual (não buscar crescer na fé)",
        "Desinteresse pelas coisas de Deus",
        "Falta de zelo apostólico (não evangelizar, não ajudar os outros na fé)",
        "Conformismo com o pecado próprio ou alheio",
        "Buscar o sucesso pessoal acima da vontade divina"
    ]
}


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = {}
    html_conteudo = ""
    if request.method == "POST":
        for mandamento, lista in pecados.items():
            indices = request.form.getlist(mandamento)
            selecionados = [lista[int(i)] for i in indices if i.isdigit() and int(i) < len(lista)]
            if selecionados:
                resultado[mandamento] = selecionados

        custom = request.form.get("custom", "").strip()
        if custom:
            resultado.setdefault("Outros pecados digitados", []).append(custom)

        html_conteudo = render_template("pdf_template.html", resultado=resultado)

    return render_template("index.html", pecados=pecados, resultado=resultado, html_conteudo=html_conteudo)

@app.route("/download", methods=["POST"])
def download():
    html_renderizado = request.form.get("html_conteudo", "")
    if not html_renderizado:
        return "Conteúdo vazio para gerar PDF", 400

    pdf_io = BytesIO()
    html = HTML(string=html_renderizado, base_url=request.base_url)
    html.write_pdf(target=pdf_io)  # Correto para novas versões
    pdf_io.seek(0)

    return Response(pdf_io.read(),
                    mimetype="application/pdf",
                    headers={"Content-Disposition": "attachment;filename=meus_pecados.pdf"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
