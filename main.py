import random
from time import sleep

PONTUACAO_MAXIMA = 1000
PERSONAGENS = ['Neymar Jr.', 'Vini Jr.', 'Ana Castela', 'Vírgina', 'Zé Felipe', 'Bruna Biancardi', 'Bruna Marquezine']
OPCOES = '\n'.join(f'[bold cyan]{index}.[/] {personagem}' for index, personagem in enumerate(PERSONAGENS))
ITENS = ['Faca de Chef', 'Garrafa de Champagne', 'Veneno', 'Taco de Sinuca', 'Peça de Diamante']
MAXIMO_INVESTIGACOES_POR_DIA = 3
TOTAL_DE_DIAS = 10
POSSIBILIDADES_INVESTIGACAO = ['PISTA', 'MORTE', 'NADA']
PROBABILIDADE_BASE_MORTE = 0
PROBABILIDADE_BASE_PISTA = 60
PROBABILIDADE_MINIMA_PISTA = 5
PROBABILIDADE_MAXIMA_MORTE = 90
MODIFICADOR_DIA_MORTE = 2
MODIFICADOR_DIA_PISTA = 3
MODIFICADOR_GANANCIA = 5

ACOES_INVESTIGACAO = [
    'Coletando digitais na maçaneta...',
    'Analisando respingos no carpete...',
    'Interrogando os funcionários do cruzeiro...',
    'Verificando as câmeras de segurança do corredor...',
    'Procurando fibras de tecido suspeitas...'
]

ACOES_DORMIR = [
    'Descansando no camarote enquanto revisa as notas...',
    'Contando ovelhas até o amanhecer...',
    'Tentando dormir com um olho aberto...',
    'O navio balança suavemente enquanto você espera o próximo dia...'
]

FRASES_NADA = [
    'Você revirou o local, mas só encontrou poeira e frustração.',
    'Tem certeza que passou na escola de investigadores? Nada útil aqui.',
    'Uma busca minuciosa não revelou nada de novo.',
    'Parece que o assassino limpou bem esta área. Nenhuma pista.'
]

FRASES_BARRADO = [
    'A assessoria do Neymar te parou: \'Você está cortando a vibe do cruzeiro. Chega por hoje.\'',
    'Um segurança de 2 metros cruzou os braços na sua frente: \'O chefe disse que já deu, parça.\'',
    'Sua presença está deixando os patrocinadores nervosos. Acesso revogado até amanhã.',
    'Muitos flashs! A gestão de imagem pediu para você \'baixar a bola\' e voltar amanhã.',
    'Você tentou investigar, mas foi cercado por fãs pedindo autógrafos achando que você era famoso. Melhor desistir por hoje.'
]

FRASES_ACUSACAO_FALSA = [
    '{palpite} estava fazendo uma live no Instagram na hora do crime com 1 milhão de testemunhas. Seu álibi é incontestável. Você virou piada na internet.',
    'Os advogados de {palpite} chegaram de helicóptero com um processo por calúnia. Enquanto isso, o verdadeiro assassino, {real}, fugiu de Jet Ski.',
    'Um silêncio constrangedor tomou o salão. {palpite} riu da sua cara: \'Eu? Jamais!\'. O verdadeiro culpado, {real}, aproveitou a confusão para escapar.',
    'Você prendeu {palpite}, mas na manhã seguinte outro crime aconteceu. O verdadeiro assassino era {real}. Sua carreira acabou.',
    'A multidão vaiou sua dedução. {palpite} é inocente. De longe, você viu {real} brindando com champagne, impune.',
    'Você confrontou {palpite} publicamente, mas ele era inocente e acabou com vc na rima. Sua reputação está arruinada. O verdadeiro assassino era: {assassino}'
]

FRASES_MORTE = [
    'Você sentiu um empurrão forte. A última coisa que viu foi a espuma do mar e {assassino} sorrindo no convés.',
    'Enquanto analisava uma pista, {assassino} surgiu das sombras com um objeto pesado. Tudo ficou escuro.',
    'Você aceitou um drink misterioso enviado por {assassino}... fim.',
    'Você entrou na sauna para investigar, mas {assassino} trancou a porta pelo lado de fora. O calor foi insuportável.',
    'Você descobriu demais. {assassino} garantiu que seu silêncio fosse eterno nas águas profundas do oceano.'
]

FRASES_VITORIA = [
    'A música parou e todos olharam para você. Ao desmascarar {assassino}, a multidão aplaudiu. O DJ soltou o som e você foi carregado nos ombros.',
    'Com {assassino} algemado no porão do navio, a festa recomeçou mais forte do que nunca. Você agora é a celebridade mais falada do cruzeiro.',
    'Você desmascarou {assassino} na frente de todos! A festa voltou a bombar. O celular do Neymar tocou e ele te passou o aparelho: \'Fala aí, detetive. O pessoal do marketing adorou sua performance. Querem saber se você faz stories com link na bio.\'',
    'Com frieza cirúrgica, você provou que {assassino} era o culpado. O navio inteiro gritou seu nome! Minutos depois, chegou o e-mail: \'Parabéns pela prisão. Aproveitando o engajamento, gostaríamos de orçar um reels de 15s divulgando odds turbinadas.\'',
    'A multidão gritou seu nome quando {assassino} foi levado. Sua dedução foi perfeita.\nNeymar piscou para você e a equipe de marketing chegou junto: \'Aproveitando o hype... que tal lançar seu curso de \'Como Ser Detetive\' nos stories agora mesmo? Arrasta pra cima!\''
]

FRASES_FIM_PRAZO = [
    'Você perdeu o [bold]timing[/]. A mídia já esqueceu o morto e agora só fala da nova dancinha do TikTok que viralizou no convés.',
    'Já é Carnaval e ninguém mais lembra do morto. A investigação caiu no esquecimento popular.',
    'O departamento de polícia entrou em recesso e só ano que vem pra continuar a investigação',
    'Prazo esgotado. O inquérito foi arquivado por \'excesso de prazo e falta de provas contundentes\'',
    'Fim da viagem! O delegado local disse que não pode assumir o caso porque o crime aconteceu em \'águas internacionais\'',
    'Acabou o prazo! A assessoria emitiu uma nota dizendo que \'o importante foi a experiência\' e te proibiu de continuar a investigação.'
]

TEXTO_REGRAS = f'''
Você é um investigador especial da polícia e tem [bold yellow]{TOTAL_DE_DIAS} dias[/] para descobrir quem foi o assassino.\n
[bold underline]DETALHES DA MISSÃO:[/]
• A cada dia, um 'X9' (uma das celebridades) te contará uma [cyan]nova pista gratuitamente[/].
• Você pode realizar até [bold cyan]{MAXIMO_INVESTIGACOES_POR_DIA} investigações extras por dia[/] para tentar forçar mais pistas.
• [bold red]CUIDADO![/] Investigações extras geram repercussão na mídia. A assessoria do Neymar não gosta disso, e o risco do assassino te notar aumenta a cada tentativa.\n
[italic]Não deixe o assassino te encontrar primeiro...[/]
'''


def carregar_cenario():
    assassino, morto, personagem1, personagem2, personagem3, personagem4, personagem5 = random.sample(PERSONAGENS, len(PERSONAGENS))
    arma_crime = random.choice(ITENS)
    contexto = (
        'Depois de uma noite de balada movimentada entre as celebridades no Cruzeiro do Neymar todos acordaram surpresos'
        f' ao saber que {morto} apareceu [b]MORTO[/] no quarto de Neymar Júnior. Os policiais isolaram a área,'
        ' levantando questões sobre como o assassino havia chegado até ali.'
        f'\n[green]Quem matou {morto}?[/]'
    )

    pista_inicial = f"O {morto} foi encontrado [red]morto[/] no quarto do Neymar."

    pistas = [
        f'Se {morto} foi morto com o(a) [b cyan]{arma_crime}[/], então ele bebeu no copo do {assassino} [b]OU[/] {personagem5} é o assassino.',
        f'Se {morto} foi morto na [b blue]Piscina Principal[/], então {personagem1} usou a [b cyan]Garrafa de Champagne[/] E {personagem2} se encontrou com {morto} antes de dormir.',
        f'Se {personagem4} estava no [cyan]Quarto do Vini JR[/] [b]E[/] estava com ferimentos causados pelo [b cyan]{arma_crime}[/], então {personagem5} [b red]NÃO[/] é o assassino.',
        f'{personagem4} estava no [cyan]Quarto do Vini Jr[/] E estava com ferimentos [b]SE E SOMENTE SE[/] a arma era o(a) [b cyan]{arma_crime}[/].',
        f'{personagem5} é o assassino [b]SE E SOMENTE SE[/] {morto} foi morto no [magenta]Salão de Jogos[/].',
        f'{assassino} matou {morto} empurrando-o para fora do navio, próximo ao [yellow]Bar do Convés[/].',
        f'Se {personagem5} tem comportamento agressivo e já machucou {personagem3}, então {personagem3} estava dormindo no [cyan]Quarto da Ana Castela[/].',
        f'Se {personagem3} \'deu um pião\' na manhã da descoberta, então ele usou o(a) [b cyan]{arma_crime}[/] para \'passar\' {morto}.',
        f'Se {personagem4} estava com ferimentos recentes, então ele estava com {personagem1} OU a arma NÃO era o(a) [b cyan]{arma_crime}[/] E {personagem2} estava nos [white]Banheiros[/].',
        f'Se {personagem4} brigou no [yellow]Restaurante[/], então {assassino} usou o(a) [b cyan]{arma_crime}[/] para matar {morto}.',
    ]

    random.shuffle(pistas)

    return assassino, contexto, pista_inicial, pistas



def main():
    c = Console(force_terminal=True)
    c.print(Panel(TEXTO_REGRAS, title="Briefing do Investigador", border_style="blue", box=box.ROUNDED))
    Confirm.ask("Pressione Enter para iniciar a investigação", console=c, show_default=False, default=True, show_choices=False)
    c.clear()
    while True:
        assassino, contexto, pista_inicial, pistas = carregar_cenario()
        pistas_encontradas = [pista_inicial]
        c.print(Panel(Text('O Mistério no Cruzeiro', justify='center')))
        c.print(Panel(contexto, title="O Crime", border_style="red", padding=(1, 2)))

        dia = 0
        investigacoes_disponiveis = MAXIMO_INVESTIGACOES_POR_DIA
        investigacao_em_andamento = True
        while investigacao_em_andamento:
            if dia == TOTAL_DE_DIAS:
                c.print(Panel(
                    f'\n[bold yellow]O CRUZEIRO ATRACOU![/]\n\n{random.choice(FRASES_FIM_PRAZO)}\n',
                    title='PRAZO ESGOTADO  :hourglass_done:',
                    border_style='yellow',
                    box=box.HEAVY_EDGE,
                    padding=(2, 5)
                ), justify='center')
                break
            modificador_dia_pista = dia * MODIFICADOR_DIA_PISTA
            modificador_dia_morte = dia * MODIFICADOR_DIA_MORTE

            modificador_ganancia = (MAXIMO_INVESTIGACOES_POR_DIA - investigacoes_disponiveis) * MODIFICADOR_GANANCIA

            prob_morte = PROBABILIDADE_BASE_MORTE + modificador_dia_morte + modificador_ganancia

            prob_pista = PROBABILIDADE_BASE_PISTA - modificador_dia_pista

            prob_pista = max(PROBABILIDADE_MINIMA_PISTA, prob_pista)
            prob_morte = min(PROBABILIDADE_MAXIMA_MORTE, prob_morte)

            c.rule(f"[bold blue]Dia {dia + 1}[/]")
            stats_table = Table(show_header=True, header_style='bold white on deep_sky_blue1', box=box.SIMPLE_HEAD)
            stats_table.add_column('Dia Atual', justify='center')
            stats_table.add_column('Investigações Restantes', justify='center')
            stats_table.add_column('Chance de Pista', justify='center')
            stats_table.add_column('Risco de Morte', justify='center')

            cor_risco = "red" if prob_morte > 50 else "yellow"
            cor_pista = "green" if prob_pista > 40 else "yellow"

            stats_table.add_row(
                f'{dia + 1}/{TOTAL_DE_DIAS}',
                f'{investigacoes_disponiveis}/{MAXIMO_INVESTIGACOES_POR_DIA}',
                f'[{cor_pista}]{prob_pista:.0f}%[/]',
                f'[{cor_risco}]{prob_morte:.0f}%[/]'
            )
            c.print(stats_table, justify='center')


            menu = Table.grid(padding=1)
            menu.add_column(style='bold cyan')
            menu.add_column(style='white')
            menu.add_row('[0] INVESTIGAR', 'Tentar encontrar pistas ativamente (Aumenta risco).')
            menu.add_row('[1] CONFRONTAR', 'Acusar o suspeito final (Encerra o jogo).')
            menu.add_row('[2] DORMIR', 'Passar para o próximo dia e receber a pista diária do X9.')

            c.print(Panel(menu, title='O que você fará agora, detetive?', border_style='blue'))
            acao = IntPrompt.ask('>>> Escolha sua ação', console=c, choices=['0', '1', '2'], show_choices=False)

            if acao == 0:
                if investigacoes_disponiveis <= 0:
                    c.print(Panel(random.choice(FRASES_BARRADO), title='[bold yellow]Ação Bloqueada[/]', border_style='yellow'))
                    sleep(1.5)
                    continue

                with Status(f'[bold blue]{random.choice(ACOES_INVESTIGACAO)}[/]', console=c):
                    sleep(2.5)
                investigacoes_disponiveis -= 1
                prob_nada = max(0, 100 - (prob_morte + prob_pista))
                pesos = [prob_pista, prob_morte, prob_nada]

                resultado = random.choices(POSSIBILIDADES_INVESTIGACAO, weights=pesos, k=1)[0]
                match resultado:
                    case 'PISTA':
                        if pistas:
                            pista_encontrada = pistas.pop()
                            pistas_encontradas.append(pista_encontrada)
                            c.print(Panel(pista_encontrada, title='[bold green]SUCESSO: Nova Pista Encontrada![/]',
                                          border_style='green', box=box.DOUBLE))
                        else:
                            c.print(
                                Panel('Você revirou tudo, mas parece que não há mais pistas para encontrar.',
                                      title='[bold yellow]Sem Mais Pistas[/]', border_style='yellow'))
                        sleep(2)
                    case 'MORTE':
                        c.clear()
                        frase_morte = random.choice(FRASES_MORTE).format(assassino=assassino)

                        c.print(Panel(
                            f'\n[bold red blink]VOCÊ MORREU![/]\n\n{frase_morte}\n',
                            title='GAME OVER', border_style='red', box=box.HEAVY_EDGE, padding=(2, 5)
                        ), justify='center')
                        investigacao_em_andamento = False
                    case 'NADA':
                        c.print(Panel(random.choice(FRASES_NADA), title='[bold yellow]Fracasso[/]', border_style='yellow'))
                        sleep(1.5)
            elif acao == 1:
                sleep(0.5)
                c.print(Panel(OPCOES, title='Lista de Suspeitos', border_style='cyan'))
                indice_assasino_palpite = IntPrompt.ask(f'[bold]Quem é o assassino?[/]', console=c,
                                                        choices=[str(i) for i in range(len(PERSONAGENS))],
                                                        show_choices=False)

                assassino_palpite = PERSONAGENS[indice_assasino_palpite]

                with Status(f'Confrontando {assassino_palpite}...', console=c, spinner='aesthetic'):
                    sleep(2)

                c.clear()

                if 0 <= indice_assasino_palpite < len(PERSONAGENS):
                    sleep(0.5)
                    assassino_palpite = PERSONAGENS[indice_assasino_palpite]
                    c.print(f'Você confrontou o {assassino_palpite}!')
                    if assassino_palpite == assassino:
                        pontuacao = PONTUACAO_MAXIMA * (1 / (dia+1))

                        texto_final = Text()
                        texto_final.append(f'{random.choice(FRASES_VITORIA).format(assassino=assassino)}\n\n')
                        texto_final.append(f'Pontuação Final: {pontuacao:.0f}/{PONTUACAO_MAXIMA}', style='bold yellow')

                        c.print(Panel(
                            texto_final,
                            title='[bold green]CASO ENCERRADO COM SUCESSO![/]',
                            border_style='bright_green',
                            box=box.DOUBLE,
                            padding=(2, 5)
                        ),justify='center')
                        investigacao_em_andamento = False
                    else:
                        frase_erro = random.choice(FRASES_ACUSACAO_FALSA).format(palpite=assassino_palpite,
                                                                                 real=assassino)
                        c.print(Panel(
                            f'\n[bold red]ACUSAÇÃO ERRADA![/]\n\n{frase_erro}\n',
                            title='GAME OVER', border_style='red', box=box.HEAVY_EDGE, padding=(2, 5)
                        ), justify='center')
                        investigacao_em_andamento = False

            elif acao == 2:
                dia += 1
                with Status(f'[bold blue]{random.choice(ACOES_DORMIR)}[/]', console=c, spinner='moon'):
                    sleep(2)
                investigacoes_disponiveis = MAXIMO_INVESTIGACOES_POR_DIA
                c.clear()
                if pistas:
                    pista_encontrada = pistas.pop()
                    pistas_encontradas.append(pista_encontrada)
                    c.print(Panel(pista_encontrada, title='[cyan]O X9 diário te enviou uma nova pista:[/]',
                                  border_style='cyan', box=box.ROUNDED))
                    sleep(2)
                else:
                    c.print(Panel('O X9 não tinha novas informações hoje.', title='[yellow]Sem Pistas do X9[/]',
                                  border_style='yellow'))

        if not Confirm.ask('\n[bold]Deseja jogar novamente?[/]', console=c, default=True):
            c.print('Até a próxima investigação, detetive.')
            break
        c.clear()

if __name__ == '__main__':
    try:
        from rich.console import Console
        from rich.status import Status
        from rich.panel import Panel
        from rich.text import Text
        from rich.prompt import IntPrompt, Confirm
        from rich.table import Table
        from rich import box
    except ImportError:
        print('Por Favor, instale utilizada a biblioteca no projeto')
        print('pip install rich')
    else:
        main()