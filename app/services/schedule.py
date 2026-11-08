from datetime import date, timedelta

TRACKS = ["Alto valor", "Compra em quantidade", "Incentivo", "Público jovem", "Geral"]
MESSAGES = {
    "Alto valor": [
        "Olá, {nome}! Você é um dos nossos clientes especiais: a partir desta semana, tem frete grátis em todos os pedidos.",
        "{nome}, separamos produtos que combinam com suas últimas compras. Confira no app.",
        "{nome}, queremos ouvir você: responda nossa pesquisa de 1 minuto e ganhe um cupom de 10%.",
    ],
    "Compra em quantidade": [
        "Olá, {nome}! Pedidos acima de 20 itens têm 5% de desconto automático.",
        "{nome}, você pode agendar a entrega para o dia que preferir. Veja como no app.",
        "{nome}, monte sua lista de compras recorrentes e receba um lembrete na hora de repor.",
    ],
    "Incentivo": [
        "Olá, {nome}! Use o cupom BEMVINDO e ganhe 15% na próxima compra.",
        "{nome}, temos produtos a partir de R$ 9,90 com entrega rápida. Aproveite para experimentar.",
        "{nome}, seu cupom de 15% expira em 7 dias. Não deixe passar!",
    ],
    "Público jovem": [
        "E aí, {nome}! Siga a gente nas redes e veja os lançamentos antes de todo mundo.",
        "{nome}, indique um amigo e vocês dois ganham R$ 20 de desconto.",
        "{nome}, chegou a nova coleção. Dá uma olhada e conta pra gente o que achou.",
    ],
    "Geral": [
        "Olá, {nome}! Obrigado por comprar com a gente. Confira as novidades da semana.",
        "{nome}, ative as notificações do app para não perder nenhuma promoção.",
        "{nome}, conta pra gente como foi sua última compra respondendo uma pesquisa rápida.",
    ],
}
WEEKDAYS = [
    "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira",
    "Sexta-feira", "Sábado", "Domingo",
]


def make_schedule(customers: list, weekday: int) -> list[dict]:
    result = []
    for customer in customers:
        start = date.fromisoformat(customer["confirmed_at"])
        start += timedelta(days=(weekday - start.weekday()) % 7)
        selected = customer["tracks"].split("|")
        week = 0
        for track in TRACKS:
            if track not in selected:
                continue
            for index, template in enumerate(MESSAGES[track]):
                scheduled = start + timedelta(weeks=week)
                first_name = customer["full_name"].split()[0]
                result.append({
                    "customer_id": customer["id"],
                    "name": customer["full_name"],
                    "phone": customer["phone"],
                    "track": track,
                    "index": index,
                    "date": scheduled.isoformat(),
                    "message": template.replace("{nome}", first_name),
                })
                week += 1
    return sorted(result, key=lambda item: (item["date"], item["customer_id"]))
