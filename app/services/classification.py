
def classify(total_value: float, total_items: int, age: int) -> list[tuple[str, str]]:
    tracks = []

    if total_value >= 10000:
        tracks.append(("Alto valor", f"valor total R$ {total_value:,.2f} ≥ R$ 10.000"))
    if total_items >= 15:
        tracks.append(("Compra em quantidade", f"{total_items} itens ≥ 15"))
    if total_value < 1000:
        tracks.append(("Incentivo", f"valor total R$ {total_value:,.2f} < R$ 1.000"))
    if age < 30:
        tracks.append(("Público jovem", f"idade {age} < 30"))

    if not tracks:
        tracks.append(("Geral", "não se encaixou em nenhuma trilha anterior"))

    return tracks