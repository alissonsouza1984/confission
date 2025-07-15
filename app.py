from flask import Flask, render_template, request, Response, url_for
from weasyprint import HTML
from io import BytesIO

app = Flask(__name__)

pecados = {
    "1. Amar a Deus sobre todas as coisas": [
        "Negligenciei minha oração diária",
        "Tive dúvidas sobre a fé e critiquei os ensinamentos da Igreja",
        "Senti desânimo espiritual e me revoltei contra Deus",
        "Frequentei cultos ou práticas supersticiosas (ex: cartomantes, horóscopos)",
        "Busquei minha própria glória em vez da vontade de Deus",
        "Fui orgulhoso, vaidoso ou apegado a elogios",
        "Apeguei-me excessivamente ao dinheiro e aos bens materiais",
        "Fui impaciente e pouco tolerante com os outros",
        "Fui indiferente diante do sofrimento alheio",
        "Faltou-me empatia e amor ao próximo",
        "Levei outros ao pecado com meus conselhos, atitudes ou exemplos",
        "Ignorei oportunidades de praticar caridade"
    ],
    "2. Não tomar o nome de Deus em vão": [
        "Usei o nome de Deus ou dos santos de forma desrespeitosa",
        "Ridicularizei símbolos da fé ou religiosos",
        "Fiz promessas sem intenção de cumprir",
        "Fiz juramentos falsos ou desnecessários",
        "Permiti ou ri quando outros zombaram da fé",
        "Usei expressões religiosas com banalidade ou em vão"
    ],
    "3. Guardar domingos e festas de guarda": [
        "Faltei à missa dominical ou em dias santos sem necessidade grave",
        "Cheguei intencionalmente atrasado à missa ou saí antes da bênção final",
        "Comunguei estando em pecado mortal",
        "Deixei de me confessar ao menos uma vez ao ano",
        "Não jejuei ou não fiz abstinência quando mandado pela Igreja",
        "Negligenciei a ajuda material à Igreja",
        "Fui à missa por obrigação, sem esforço de viver a fé no dia a dia"
    ],
    "4. Honrar pai e mãe": [
        "Desobedeci e faltei com respeito aos meus pais ou superiores",
        "Negligenciei os cuidados com meus pais idosos ou doentes",
        "Maltratei meu cônjuge com palavras ou atitudes",
        "Dei mau exemplo aos meus filhos",
        "Permiti influências negativas sobre meus filhos (TV, internet, amizades)",
        "Fui negligente na formação religiosa dos meus filhos",
        "Deixei de corrigir meus filhos por comodismo",
        "Fui ingrato com meus pais ou avós"
    ],
    "5. Não matar": [
        "Alimentei ódio, rancor, inimizade ou desejo de vingança",
        "Recusei-me a perdoar",
        "Desejei a morte ou o mal a alguém (ou a mim mesmo)",
        "Apoiei ou pratiquei aborto, eutanásia ou outras práticas semelhantes",
        "Fui descuidado com minha saúde (excesso de comida, drogas, bebida, sedentarismo)",
        "Assumi riscos desnecessários à minha vida (direção imprudente, vícios)",
        "Dei escândalo ou mau exemplo",
        "Proferi palavrões ou palavras agressivas contra os outros",
        "Feri emocionalmente alguém com minhas palavras ou atitudes",
        "Fui violento, mesmo verbalmente, com pessoas próximas"
    ],
    "6. Não pecar contra a castidade": [
        "Consenti em pensamentos ou desejos impuros",
        "Me masturbei, assisti pornografia ou tive relações sexuais fora do casamento",
        "Fui infiel emocionalmente ou fisicamente",
        "Tive liberdades excessivas no namoro",
        "Usei roupas provocativas com má intenção",
        "Participei de conversas ou fiz piadas imorais",
        "Consumi conteúdo sexualizado (TV, filmes, redes sociais)",
        "Mantive amizades que me levaram ao pecado",
        "Fiz comentários maliciosos sobre o corpo de outras pessoas",
        "Alimentei fantasias sexuais intencionalmente"
    ],
    "7. Não roubar": [
        "Roubei ou fui desonesto em contratos ou negócios",
        "Me apropriei de bens ou dinheiro indevidamente",
        "Deixei de pagar dívidas justas ou salários devidos",
        "Desperdicei tempo no trabalho ou trabalhei com negligência",
        "Fui viciado em jogos de azar",
        "Vivi acima dos meus meios",
        "Fui injusto ao cobrar ou receber valores excessivos",
        "Usei benefícios ou ajudas indevidamente"
    ],
    "8. Não levantar falso testemunho": [
        "Menti habitualmente, mesmo sem prejudicar diretamente",
        "Caluniei, difamei ou exagerei defeitos dos outros",
        "Ouvi ou espalhei boatos",
        "Julguei mal ou condenei injustamente alguém",
        "Causei divisão entre pessoas por fofoca",
        "Não reparei a má reputação causada por mim",
        "Fui hipócrita ou dissimulado para parecer melhor"
    ],
    "9. Não desejar a mulher do próximo": [
        "Alimentei desejos impuros por pessoas casadas ou consagradas",
        "Tive fantasias ou intenções de infidelidade",
        "Assediei verbal ou fisicamente",
        "Flertei com pessoas comprometidas",
        "Tive curiosidade indevida sobre a intimidade de outras pessoas",
        "Usei o olhar de maneira impura ou desrespeitosa"
    ],
    "10. Não cobiçar as coisas alheias": [
        "Invejei os bens, o sucesso ou os talentos dos outros",
        "Desejei tomar ou imitar aquilo que pertence a outros",
        "Fiquei descontente com a minha vida por causa de comparações",
        "Fui ambicioso em excesso, sem gratidão pelo que tenho",
        "Desejei viver a vida dos outros em vez de valorizar a minha"
    ],
    "Mandamentos da Igreja": [
        "Faltei à Missa em festas de guarda",
        "Não me confessei ao menos uma vez por ano",
        "Não comunguei na Páscoa",
        "Comunguei em pecado grave",
        "Não guardei jejum e abstinência nos tempos prescritos",
        "Não ajudei a Igreja materialmente",
        "Desprezei os sacramentos por comodismo ou frieza espiritual"
    ],
    "Pecados relacionados ao casamento e à família": [
        "Fui negligente com meu cônjuge (no diálogo, carinho ou atenção)",
        "Fui violento física ou verbalmente dentro do lar",
        "Desrespeitei meu cônjuge",
        "Guardei mágoas e não perdoei no matrimônio",
        "Priorizei trabalho ou lazer em detrimento da família",
        "Recusei-me a ter filhos sem justa causa",
        "Não dei testemunho cristão dentro do lar",
        "Fui indiferente à vida familiar ou às necessidades dos meus",
        "Usei palavras ofensivas ou humilhantes com meus familiares"
    ],
    "Pecados espirituais e morais": [
        "Fui preguiçoso espiritualmente (não busquei crescer na fé)",
        "Me desinteressei pelas coisas de Deus",
        "Fui indiferente no zelo apostólico (não evangelizei, nem ajudei outros na fé)",
        "Fui conivente com o pecado, meu ou alheio",
        "Busquei o sucesso pessoal acima da vontade divina",
        "Agi por egoísmo, pensando apenas em mim",
        "Fui omisso diante de injustiças ou sofrimentos ao meu redor"
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
