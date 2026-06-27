import base64
import csv
import html
import io
import json
import random
import uuid
from datetime import datetime
from pathlib import Path

import streamlit as st


APP_TITLE = "Misión Nutrición: Salvando al Paciente"
RESULTS_FILE = Path("resultados.json")
HERO_IMAGE = Path("assets") / "aaaaagen.png"
SHEET_HEADERS = ["attempt_id", "team", "patient", "score", "health", "status", "submitted_at"]


def image_data_uri(path):
    try:
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    except OSError:
        return ""
    return f"data:image/png;base64,{encoded}"

PATIENTS = [
    {
        "name": "Paciente A: Mujer con cansancio y palidez",
        "age": "25 años",
        "reason": "Consulta por cansancio persistente y mareos.",
        "symptoms": ["Cansancio", "Palidez", "Mareos", "Bajo consumo de carnes"],
        "habits": "Consume pocas legumbres y casi no combina alimentos con vitamina C.",
        "vitals": {"Energía": "Baja", "Apetito": "Regular", "Riesgo": "Moderado"},
        "case": "Mujer de 25 años con cansancio, palidez, mareos y bajo consumo de carnes y legumbres.",
        "diagnosis": "Anemia",
        "foods_good": ["Lentejas", "Hígado", "Espinaca", "Carne roja", "Frijoles"],
        "foods_bad": ["Gaseosa", "Dulces", "Frituras", "Pollo", "Leche", "Vino tinto"],
        "advice": "Consumir alimentos ricos en hierro y combinarlos con vitamina C para mejorar la absorción.",
    },
    {
        "name": "Paciente B: Adulto con sed frecuente",
        "age": "45 años",
        "reason": "Consulta por sed frecuente y cansancio después de las comidas.",
        "symptoms": ["Mucha sed", "Cansancio después de comer", "Gaseosas frecuentes", "Dulces frecuentes"],
        "habits": "Toma bebidas azucaradas casi a diario y consume postres varias veces por semana.",
        "vitals": {"Energía": "Media-baja", "Apetito": "Variable", "Riesgo": "Alto"},
        "case": "Adulto de 45 años con mucha sed, cansancio después de las comidas, consumo frecuente de gaseosas y dulces.",
        "diagnosis": "Diabetes",
        "foods_good": ["Avena", "Verduras", "Manzana", "Pescado", "Legumbres", "Pechuga de pollo", "Queso criollo"],
        "foods_bad": ["Gaseosa", "Pasteles", "Caramelos", "Arroz blanco", "Pan blanco", "Leche entera", "Queso cheddar"],
        "advice": "Reducir azúcares simples, elegir alimentos con fibra soluble y controlar las porciones.",
    },
    {
        "name": "Paciente C: Niño con exceso de peso",
        "age": "10 años",
        "reason": "Consulta por aumento de peso, dolor de rodillas y bajo consumo de frutas.",
        "symptoms": ["Exceso de peso", "Dolor de rodillas", "Poca fruta", "Comida rápida"],
        "habits": "Prefiere comida rápida y pasa mucho tiempo sentado después de clases.",
        "vitals": {"Energía": "Regular", "Apetito": "Alto", "Riesgo": "Moderado"},
        "case": "Niño de 10 años con aumento de peso, dolor de rodillas, bajo consumo de frutas y alta ingesta de comida rápida.",
        "diagnosis": "Obesidad",
        "foods_good": ["Frutas", "Verduras", "Pollo a la plancha", "Agua", "Yogur natural", "Huevo", "Pescado blanco", "Palta"],
        "foods_bad": ["Hamburguesa", "Papas fritas light", "Gaseosa cero azúcar"],
        "advice": "Promover alimentación equilibrada, actividad física y reducir ultraprocesados.",
    },
    {
        "name": "Paciente D: Adulto con presión alta",
        "age": "55 años",
        "reason": "Consulta por dolor de cabeza matinal y controles repetidos con presión elevada.",
        "symptoms": ["Presión alta", "Dolor de cabeza", "Alimentos salados", "Alcohol frecuente"],
        "habits": "Fuma, consume alcohol varias veces por semana y come productos salados con frecuencia.",
        "vitals": {"Energía": "Regular", "Apetito": "Normal", "Riesgo": "Alto"},
        "case": "Adulto de 55 años con dolores de cabeza por las mañanas, fuma y consume alcohol varias veces a la semana, además tiene la presión arterial elevada y consumo frecuente de alimentos salados.",
        "diagnosis": "Hipertensión",
        "foods_good": ["Plátano", "Brócoli", "Avena", "Pollo sin piel", "Agua", "Arroz integral"],
        "foods_bad": ["Picana", "Asado de tira", "Embutidos", "Sopas instantáneas", "Snacks salados", "Leche entera"],
        "advice": "Disminuir el consumo de sal, evitar embutidos y aumentar frutas, verduras y carnes sin grasa.",
    },
]

SURPRISE_CARDS = [
    ("El paciente siguió la recomendación nutricional. +10 puntos", 10),
    ("El paciente olvidó tomar agua suficiente. -5 puntos", -5),
    ("El equipo explicó muy bien el caso. +10 puntos", 10),
    ("El paciente consumió comida chatarra. -10 puntos", -10),
    ("El paciente realizó actividad física. +5 puntos", 5),
    ("Hubo confusión en el diagnóstico. -5 puntos", -5),
]

ROLES = [
    "Nutricionista líder: decide el diagnóstico final.",
    "Evaluador de alimentos: elige alimentos recomendados y no recomendados.",
    "Diseñador del plato: arma la propuesta de alimentación.",
    "Comunicador: explica la recomendación final al paciente.",
]

CREDITS = {
    "lema": "Si puedes imaginarlo, puedes programarlo.",
    "design": "Raúl Limachi H.",
    "collaborators": [
        "Axel Ferrufino",
        "Briceyla Yujra Nina",
        "Fabio Gutiérrez Portillo",
        "Jamelin Ricela",
        "Rebeca Pezas Álvarez",
        "Ximena Flores",
        "Madeliz Tania Sinani Quispe",
    ],
}


st.set_page_config(page_title=APP_TITLE, page_icon=":hospital:", layout="wide")


def init_state():
    defaults = {
        "screen": "start",
        "return_screen": "start",
        "attempt_id": "",
        "team_name": "",
        "score": 0,
        "patient_health": 50,
        "patient_index": None,
        "selected_diagnosis": "",
        "food_options": [],
        "last_message": "",
        "surprise_text": "",
        "submitted": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def set_screen(screen):
    st.session_state.screen = screen
    st.rerun()


def go_ranking():
    if st.session_state.screen != "ranking":
        st.session_state.return_screen = st.session_state.screen
    set_screen("ranking")


def load_results():
    if google_sheets_enabled():
        return load_results_from_sheet()

    if not RESULTS_FILE.exists():
        return []
    try:
        data = json.loads(RESULTS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return data if isinstance(data, list) else []


def save_results(results):
    if google_sheets_enabled():
        save_results_to_sheet(results)
        return

    RESULTS_FILE.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def add_result(result):
    if google_sheets_enabled():
        add_result_to_sheet(result)
        return

    results = load_results()
    results = [item for item in results if item.get("attempt_id") != result["attempt_id"]]
    results.append(result)
    save_results(results)


def google_sheets_enabled():
    try:
        return "gcp_service_account" in st.secrets and "google_sheet_id" in st.secrets
    except Exception:
        return False


def get_google_worksheet():
    import gspread

    credentials = dict(st.secrets["gcp_service_account"])
    client = gspread.service_account_from_dict(credentials)
    spreadsheet = client.open_by_key(st.secrets["google_sheet_id"])
    worksheet_name = st.secrets.get("google_worksheet", "ranking")

    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=200, cols=len(SHEET_HEADERS))

    values = worksheet.get_all_values()
    if not values:
        worksheet.append_row(SHEET_HEADERS)
    return worksheet


def normalize_sheet_row(row):
    result = {key: row.get(key, "") for key in SHEET_HEADERS}
    for numeric_key in ["score", "health"]:
        try:
            result[numeric_key] = int(result[numeric_key])
        except (TypeError, ValueError):
            result[numeric_key] = 0
    return result


def load_results_from_sheet():
    try:
        worksheet = get_google_worksheet()
        return [normalize_sheet_row(row) for row in worksheet.get_all_records()]
    except Exception as error:
        st.warning(f"No se pudo leer Google Sheets. Usando ranking local. Detalle: {error}")
        return load_results_from_file()


def load_results_from_file():
    if not RESULTS_FILE.exists():
        return []
    try:
        data = json.loads(RESULTS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return data if isinstance(data, list) else []


def save_results_to_sheet(results):
    worksheet = get_google_worksheet()
    rows = [
        [
            result.get("attempt_id", ""),
            result.get("team", ""),
            result.get("patient", ""),
            result.get("score", 0),
            result.get("health", 0),
            result.get("status", ""),
            result.get("submitted_at", ""),
        ]
        for result in results
    ]
    worksheet.clear()
    worksheet.update([SHEET_HEADERS] + rows)


def add_result_to_sheet(result):
    try:
        results = load_results_from_sheet()
        results = [item for item in results if item.get("attempt_id") != result["attempt_id"]]
        results.append(result)
        save_results_to_sheet(results)
    except Exception as error:
        st.warning(f"No se pudo guardar en Google Sheets. Se guardara localmente. Detalle: {error}")
        results = load_results_from_file()
        results = [item for item in results if item.get("attempt_id") != result["attempt_id"]]
        results.append(result)
        RESULTS_FILE.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")


def sorted_results():
    return sorted(
        load_results(),
        key=lambda result: (result.get("score", 0), result.get("health", 0), result.get("submitted_at", "")),
        reverse=True,
    )


def csv_cell(value):
    text = str(value or "")
    if text.startswith(("=", "+", "-", "@", "\t")):
        return "'" + text
    return text


def ranking_csv(results):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Puesto", "Grupo", "Paciente", "Puntaje", "Estado del paciente", "Resultado", "Hora"])
    for position, result in enumerate(results, start=1):
        writer.writerow(
            [
                position,
                csv_cell(result.get("team", "")),
                csv_cell(result.get("patient", "")),
                result.get("score", 0),
                f"{result.get('health', 0)}%",
                csv_cell(result.get("status", "")),
                csv_cell(result.get("submitted_at", "")),
            ]
        )
    return output.getvalue().encode("utf-8-sig")


def current_patient():
    return PATIENTS[st.session_state.patient_index]


def start_game(team_name):
    team_name = team_name.strip()
    if not team_name:
        st.session_state.last_message = "Escribe el nombre de tu grupo para iniciar."
        return

    st.session_state.team_name = team_name
    st.session_state.attempt_id = str(uuid.uuid4())
    st.session_state.patient_index = random.randrange(len(PATIENTS))
    st.session_state.score = 0
    st.session_state.patient_health = 50
    st.session_state.selected_diagnosis = ""
    st.session_state.food_options = []
    st.session_state.last_message = ""
    st.session_state.surprise_text = ""
    st.session_state.submitted = False
    set_screen("arrival")


def check_diagnosis():
    selected = st.session_state.selected_diagnosis
    if not selected:
        st.session_state.last_message = "Selecciona un diagnóstico antes de continuar."
        return

    patient = current_patient()
    if selected == patient["diagnosis"]:
        st.session_state.score += 20
        st.session_state.patient_health += 15
        st.session_state.last_message = "Correcto. Diagnóstico correcto. +20 puntos."
    else:
        st.session_state.score -= 5
        st.session_state.patient_health -= 10
        st.session_state.last_message = f"Revisar. El diagnóstico correcto era: {patient['diagnosis']}."
    set_screen("foods")


def choose_diagnosis(option):
    st.session_state.selected_diagnosis = option
    check_diagnosis()


def prepare_foods():
    if st.session_state.food_options:
        return

    patient = current_patient()
    good_count = min(4, len(patient["foods_good"]))
    bad_count = min(4, len(patient["foods_bad"]))
    options = random.sample(patient["foods_good"], good_count) + random.sample(patient["foods_bad"], bad_count)
    random.shuffle(options)
    st.session_state.food_options = options
    for food in options:
        st.session_state[f"food_{food}"] = False


def toggle_food(food):
    key = f"food_{food}"
    selected = st.session_state.get(key, False)
    if selected:
        st.session_state[key] = False
        return

    chosen_count = sum(
        1
        for option in st.session_state.food_options
        if st.session_state.get(f"food_{option}", False)
    )
    if chosen_count >= 3:
        st.session_state.last_message = "La canasta ya tiene 3 alimentos. Quita uno antes de agregar otro."
        return

    st.session_state[key] = True
    st.session_state.last_message = ""


def check_foods():
    patient = current_patient()
    chosen = [
        food
        for food in st.session_state.food_options
        if st.session_state.get(f"food_{food}", False)
    ]
    good_chosen = [food for food in chosen if food in patient["foods_good"]]

    if len(chosen) == 3 and len(good_chosen) == 3:
        st.session_state.score += 25
        st.session_state.patient_health += 20
        st.session_state.last_message = "Excelente. Elegiste alimentos adecuados. +25 puntos."
    else:
        st.session_state.score -= 5
        st.session_state.patient_health -= 10
        st.session_state.last_message = "Revisar. Deben elegir 3 alimentos recomendados y evitar los no recomendados."
    set_screen("plate")


def selected_foods():
    return [
        food
        for food in st.session_state.food_options
        if st.session_state.get(f"food_{food}", False)
    ]


def plate_review():
    patient = current_patient()
    chosen = selected_foods()
    good_chosen = [food for food in chosen if food in patient["foods_good"]]
    bad_chosen = [food for food in chosen if food in patient["foods_bad"]]

    if len(chosen) != 3:
        return 0, "Plato incompleto", "La canasta no tiene exactamente 3 alimentos."
    if len(good_chosen) == 3:
        return 20, "Plato excelente", "Los 3 alimentos ayudan al caso del paciente."
    if len(good_chosen) == 2:
        return 10, "Plato aceptable", f"Hay 2 alimentos adecuados, pero deben revisar: {', '.join(bad_chosen)}."
    return 0, "Plato incompleto", "La mayoria de alimentos no corresponde al tratamiento nutricional."


def plate_score(points):
    st.session_state.score += points
    st.session_state.patient_health += points // 2
    text, surprise_points = random.choice(SURPRISE_CARDS)
    st.session_state.score += surprise_points
    st.session_state.patient_health = max(
        0,
        min(100, st.session_state.patient_health + surprise_points),
    )
    st.session_state.surprise_text = text
    set_screen("surprise")


def classify_result():
    st.session_state.patient_health = max(0, min(100, st.session_state.patient_health))
    if st.session_state.patient_health >= 75:
        return (
            "Paciente sano",
            "#2f7d32",
            "El tratamiento funciono y el paciente sale estable.",
        )
    if st.session_state.patient_health >= 45:
        return (
            "Paciente en observacion",
            "#946200",
            "El paciente mejora, pero necesita seguimiento.",
        )
    return (
        "Emergencia nutricional",
        "#a93535",
        "El paciente queda en estado critico y requiere intervencion urgente.",
    )


def submit_result_once():
    if st.session_state.submitted:
        return

    patient = current_patient()
    status, _, _ = classify_result()
    add_result(
        {
            "attempt_id": st.session_state.attempt_id,
            "team": st.session_state.team_name,
            "patient": patient["name"],
            "score": st.session_state.score,
            "health": st.session_state.patient_health,
            "status": status,
            "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )
    st.session_state.submitted = True


def reset_my_game():
    keep_message = st.session_state.get("last_message", "")
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_state()
    st.session_state.last_message = keep_message
    st.rerun()


def inject_css():
    hero_background = image_data_uri(HERO_IMAGE)
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #f4f7f2 0%, #edf6f2 54%, #f8faf7 100%);
            color: #24352f;
        }
        section[data-testid="stSidebar"] { display: none; }
        .block-container {
            max-width: 1100px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        .top-actions {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 1rem;
        }
        .top-actions h1 {
            margin: 0;
            color: #173b2f;
            font-size: 2.45rem;
            line-height: 1.04;
        }
        .top-actions p {
            margin: .4rem 0 0;
            color: #395148;
            font-size: 1rem;
        }
        .status-bar {
            display: flex;
            flex-wrap: wrap;
            gap: .55rem;
            margin: .75rem 0 1.15rem;
        }
        .pill {
            padding: .6rem .8rem;
            border: 1px solid #d2e0d9;
            border-radius: 8px;
            background: #ffffff;
            color: #173b2f;
            font-weight: 800;
            box-shadow: 0 8px 20px rgba(23, 59, 47, .08);
        }
        .panel {
            background: rgba(255, 255, 255, .94);
            border: 1px solid #dce7e1;
            border-radius: 8px;
            padding: 1.2rem;
            box-shadow: 0 16px 36px rgba(23, 59, 47, .09);
        }
        .panel h2, .panel h3 {
            margin-top: 0;
            color: #173b2f;
        }
        .roles {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: .65rem;
        }
        .role {
            padding: .85rem;
            border-radius: 8px;
            border: 1px solid #cfe2d8;
            background: #edf6f2;
            font-weight: 700;
            color: #24352f;
        }
        .diagnosis-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: .85rem;
            margin: .8rem 0 1rem;
        }
        .diagnosis-card {
            min-height: 170px;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #cfe0dc;
            background: linear-gradient(180deg, #ffffff 0%, #eef7f3 100%);
            box-shadow: 0 12px 26px rgba(23, 59, 47, .08);
        }
        .diagnosis-card h3 {
            margin: 0 0 .45rem;
            color: #173b2f;
            font-size: 1.25rem;
        }
        .diagnosis-card p {
            margin: 0;
            color: #40564d;
            font-weight: 650;
            line-height: 1.35;
        }
        .mission-alert {
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #bad8d0;
            background: #fffdf3;
            color: #173b2f;
            font-weight: 800;
            box-shadow: 0 10px 22px rgba(23, 59, 47, .07);
        }
        .market-top {
            display: grid;
            grid-template-columns: 1fr 280px;
            gap: 1rem;
            align-items: stretch;
            margin-bottom: 1rem;
        }
        .basket {
            border: 1px solid #cfe0dc;
            border-radius: 8px;
            background: #173b2f;
            color: #ffffff;
            padding: 1rem;
            box-shadow: 0 16px 32px rgba(23, 59, 47, .14);
        }
        .basket h3 {
            margin: 0 0 .5rem;
            color: #ffffff;
        }
        .basket p {
            margin: .25rem 0;
            color: #dfece7;
            font-weight: 700;
        }
        .basket-count {
            display: inline-block;
            margin: .35rem 0 .7rem;
            padding: .4rem .55rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, .12);
            color: #ffffff;
            font-weight: 950;
        }
        .basket-slots {
            display: grid;
            gap: .45rem;
        }
        .basket-slot {
            min-height: 36px;
            padding: .5rem .6rem;
            border-radius: 7px;
            border: 1px dashed rgba(255, 255, 255, .45);
            color: #ffffff;
            font-weight: 850;
            background: rgba(255, 255, 255, .08);
        }
        .basket-slot.empty {
            color: #b9d0c7;
            font-weight: 750;
        }
        .food-card {
            min-height: 168px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            border: 1px solid #d8e7e1;
            border-radius: 8px;
            background: #ffffff;
            padding: .95rem;
            box-shadow: 0 12px 28px rgba(23, 59, 47, .08);
        }
        .food-card.selected {
            border-color: #2f7d32;
            background: linear-gradient(180deg, #ffffff 0%, #edf8ef 100%);
            box-shadow: 0 14px 30px rgba(47, 125, 50, .16);
        }
        .food-icon {
            width: 44px;
            height: 44px;
            display: grid;
            place-items: center;
            border-radius: 8px;
            background: #edf6f2;
            font-size: 1.35rem;
            margin-bottom: .65rem;
        }
        .food-card h3 {
            margin: 0 0 .35rem;
            color: #173b2f;
            font-size: 1.08rem;
        }
        .food-card p {
            margin: 0;
            color: #53655e;
            font-weight: 700;
            line-height: 1.35;
        }
        .food-status {
            margin-top: .7rem;
            display: inline-block;
            padding: .35rem .5rem;
            border-radius: 999px;
            background: #f4f7f2;
            color: #173b2f;
            font-size: .85rem;
            font-weight: 900;
        }
        .ranking-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 .55rem;
            margin: 1rem 0;
        }
        .ranking-table th {
            text-align: left;
            padding: .75rem;
            color: #53655e;
            font-size: .85rem;
            text-transform: uppercase;
            letter-spacing: .04em;
        }
        .ranking-table td {
            padding: .9rem .75rem;
            background: #ffffff;
            border-top: 1px solid #dce7e1;
            border-bottom: 1px solid #dce7e1;
            color: #173b2f;
            font-weight: 750;
        }
        .ranking-table td:first-child {
            border-left: 1px solid #dce7e1;
            border-radius: 8px 0 0 8px;
            font-size: 1.2rem;
            font-weight: 900;
        }
        .ranking-table td:last-child {
            border-right: 1px solid #dce7e1;
            border-radius: 0 8px 8px 0;
        }
        .rank-first td {
            background: #fff9df;
            border-color: #ecd47f;
        }
        .score-cell {
            font-size: 1.15rem;
            color: #2f7d32 !important;
            font-weight: 950 !important;
        }
        .ranking-wrap {
            overflow-x: auto;
        }
        .teacher-panel {
            margin-top: 1rem;
            border: 1px solid #cfe0dc;
            border-radius: 8px;
            background: #ffffff;
            padding: 1rem;
            box-shadow: 0 14px 30px rgba(23, 59, 47, .08);
        }
        .teacher-panel h3 {
            margin: 0 0 .45rem;
            color: #173b2f;
        }
        .plate-guide {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .85rem;
            margin: 1rem 0;
        }
        .plate-part {
            border: 1px solid #dce7e1;
            border-radius: 8px;
            background: #ffffff;
            padding: 1rem;
            min-height: 120px;
            box-shadow: 0 10px 22px rgba(23, 59, 47, .07);
        }
        .plate-part strong {
            display: block;
            color: #173b2f;
            font-size: 1.3rem;
            margin-bottom: .35rem;
        }
        .plate-part span {
            color: #53655e;
            font-weight: 750;
        }
        .plate-review {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .85rem;
            margin: 1rem 0;
        }
        .review-food {
            border: 1px solid #dce7e1;
            border-radius: 8px;
            background: #ffffff;
            padding: 1rem;
            min-height: 130px;
            box-shadow: 0 10px 22px rgba(23, 59, 47, .07);
        }
        .review-food.good {
            border-color: #8bc78e;
            background: #f2fbf3;
        }
        .review-food.bad {
            border-color: #e1a0a0;
            background: #fff4f4;
        }
        .review-food h3 {
            margin: .45rem 0 .25rem;
            color: #173b2f;
        }
        .review-badge {
            display: inline-block;
            padding: .35rem .5rem;
            border-radius: 999px;
            background: #edf6f2;
            color: #173b2f;
            font-size: .85rem;
            font-weight: 900;
        }
        .credits-box {
            border: 1px solid #dce7e1;
            border-radius: 8px;
            background: #ffffff;
            padding: .9rem;
            box-shadow: 0 12px 26px rgba(23, 59, 47, .08);
        }
        .credits-box h3 {
            margin: 0 0 .45rem;
            color: #173b2f;
        }
        .credits-box p {
            margin: .35rem 0;
            color: #40564d;
            font-weight: 750;
        }
        .credits-box ul {
            margin: .55rem 0 0;
            padding-left: 1.1rem;
            color: #173b2f;
            font-weight: 750;
        }
        .chart {
            position: relative;
            border: 1px solid #cddfd8;
            border-radius: 8px;
            background: #ffffff;
            box-shadow: 0 18px 38px rgba(23, 59, 47, .1);
            overflow: hidden;
        }
        .chart:before {
            content: "";
            display: block;
            height: 14px;
            background: linear-gradient(90deg, #173b2f 0 28%, #2f7d32 28% 48%, #d94b4b 48% 58%, #f3c969 58% 100%);
        }
        .chart-head {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            padding: 1rem 1.15rem;
            border-bottom: 1px solid #e3ece7;
            background: #f8fbf9;
        }
        .chart-head h2 {
            margin: 0;
            color: #173b2f;
        }
        .chart-id {
            padding: .55rem .75rem;
            border-radius: 8px;
            border: 1px solid #cfe2d8;
            background: #ffffff;
            color: #173b2f;
            font-weight: 900;
            white-space: nowrap;
        }
        .chart-grid {
            display: grid;
            grid-template-columns: 1.05fr .95fr;
            gap: 1rem;
            padding: 1.15rem;
        }
        .chart-section {
            border: 1px solid #e1ebe6;
            border-radius: 8px;
            padding: .95rem;
            background: #ffffff;
        }
        .chart-section h3 {
            margin: 0 0 .65rem;
            color: #173b2f;
            font-size: 1.05rem;
            text-transform: uppercase;
            letter-spacing: .04em;
        }
        .chart-line {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            padding: .52rem 0;
            border-bottom: 1px solid #eef4f1;
        }
        .chart-line:last-child {
            border-bottom: 0;
        }
        .chart-line span {
            color: #53655e;
            font-weight: 750;
        }
        .chart-line strong {
            color: #173b2f;
            text-align: right;
        }
        .tag-list {
            display: flex;
            flex-wrap: wrap;
            gap: .5rem;
        }
        .clinical-tag {
            padding: .5rem .65rem;
            border-radius: 999px;
            background: #edf6f2;
            border: 1px solid #cfe2d8;
            color: #173b2f;
            font-weight: 800;
        }
        .note {
            margin-top: 1rem;
            padding: .95rem;
            border-radius: 8px;
            border: 1px solid #eadc9d;
            background: #fffbea;
            color: #173b2f;
            font-weight: 800;
        }
        .stRadio label,
        .stCheckbox label,
        .stTextInput label,
        [data-testid="stWidgetLabel"],
        [data-testid="stMarkdownContainer"] p {
            color: #173b2f !important;
        }
        .step-list {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .65rem;
            margin-top: .8rem;
        }
        .step {
            padding: .85rem;
            border-radius: 8px;
            background: #ffffff;
            border: 1px solid #dce7e1;
            font-weight: 800;
        }
        .hospital-scene {
            position: relative;
            overflow: hidden;
            min-height: 355px;
            border-radius: 8px;
            border: 1px solid #cfe0dc;
            background:
                linear-gradient(180deg, rgba(255,255,255,.58), rgba(255,255,255,.24)),
                repeating-linear-gradient(90deg, transparent 0 92px, rgba(72,108,102,.11) 92px 94px),
                linear-gradient(180deg, #eef6f2 0 74%, #d9e7dc 74% 100%);
            box-shadow: inset 0 -34px 0 rgba(111,138,128,.16);
        }
        .consult-door {
            position: absolute;
            left: 42px;
            bottom: 82px;
            width: 128px;
            height: 180px;
            border: 3px solid #9eb3c4;
            background: #d7e4ef;
        }
        .consult-door:before {
            content: "CONSULTA";
            position: absolute;
            top: -34px;
            left: 7px;
            color: #173b2f;
            font-weight: 900;
        }
        .bed {
            position: absolute;
            right: 62px;
            bottom: 90px;
            width: 290px;
            height: 48px;
            border: 4px solid #6f8a80;
            background: #ffffff;
        }
        .bed:before {
            content: "";
            position: absolute;
            left: 28px;
            top: -34px;
            width: 170px;
            height: 32px;
            border: 2px solid #6f8a80;
            background: #b8d7ff;
        }
        .cross-card {
            position: absolute;
            left: 45%;
            top: 70px;
            width: 160px;
            height: 98px;
            border: 2px solid #abc4bc;
            background: #ffffff;
            transform: translateX(-50%);
        }
        .cross-card:before,
        .cross-card:after {
            content: "";
            position: absolute;
            background: #d94b4b;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
        }
        .cross-card:before { width: 70px; height: 12px; }
        .cross-card:after { width: 12px; height: 70px; }
        .patient-runner {
            position: absolute;
            left: -120px;
            bottom: 52px;
            width: 110px;
            height: 190px;
            animation: arrive 2.85s ease-in-out forwards;
        }
        .head {
            position: absolute;
            left: 35px;
            top: 10px;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            border: 2px solid #8d6e63;
            background: #f0c7a5;
        }
        .torso {
            position: absolute;
            left: 40px;
            top: 55px;
            width: 35px;
            height: 75px;
            border: 2px solid #28638f;
            background: #64b5f6;
        }
        .arm-l, .arm-r, .leg-l, .leg-r {
            position: absolute;
            background: #28638f;
            border-radius: 999px;
            transform-origin: top center;
        }
        .arm-l { left: 31px; top: 74px; width: 8px; height: 48px; transform: rotate(42deg); }
        .arm-r { left: 76px; top: 74px; width: 8px; height: 48px; transform: rotate(-42deg); }
        .leg-l, .leg-r { top: 127px; width: 9px; height: 62px; background: #263238; }
        .leg-l { left: 43px; transform: rotate(18deg); }
        .leg-r { left: 63px; transform: rotate(-18deg); }
        .scene-caption {
            position: absolute;
            left: 50%;
            bottom: 18px;
            transform: translateX(-50%);
            padding: .65rem .9rem;
            border-radius: 8px;
            background: #ffffff;
            color: #173b2f;
            font-weight: 900;
            border: 1px solid #d7e5df;
            box-shadow: 0 10px 22px rgba(23, 59, 47, .11);
            text-align: center;
        }
        .result-scene .patient-runner {
            left: auto;
            right: 160px;
            bottom: 70px;
            animation: patientPulse 1.1s ease-in-out infinite;
        }
        .monitor {
            position: absolute;
            left: 92px;
            top: 74px;
            width: 170px;
            height: 116px;
            border: 2px solid #abc4bc;
            background: #ffffff;
            display: grid;
            place-items: center;
            color: var(--result-color);
            font-size: 2.1rem;
            font-weight: 900;
        }
        .ecg {
            position: absolute;
            left: 318px;
            top: 116px;
            width: 160px;
            height: 55px;
            background:
                linear-gradient(90deg, transparent 0 8%, var(--result-color) 8% 11%, transparent 11% 22%,
                var(--result-color) 22% 25%, transparent 25% 32%, var(--result-color) 32% 35%,
                transparent 35% 60%, var(--result-color) 60% 63%, transparent 63% 100%);
            animation: ecgMove 1s linear infinite;
            opacity: .8;
        }
        div.stButton > button {
            width: 100%;
            min-height: 3rem;
            border-radius: 8px;
            border: 1px solid #b6cbc3;
            background: #ffffff;
            color: #173b2f;
            font-weight: 800;
            box-shadow: 0 8px 18px rgba(23, 59, 47, .08);
        }
        div.stButton > button:hover {
            border-color: #2f7d32;
            color: #173b2f;
            background: #edf6f2;
        }
        @keyframes arrive {
            0% { transform: translateX(0) translateY(0); opacity: 0; }
            20% { opacity: 1; }
            45% { transform: translateX(310px) translateY(-8px); }
            72% { transform: translateX(560px) translateY(4px); }
            100% { transform: translateX(640px) translateY(0); opacity: 1; }
        }
        @keyframes patientPulse {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        @keyframes ecgMove {
            from { transform: translateX(-18px); }
            to { transform: translateX(18px); }
        }
        @media (max-width: 760px) {
            .top-actions { flex-direction: column; }
            .top-actions h1 { font-size: 2rem; }
            .roles, .step-list, .diagnosis-grid, .chart-grid, .market-top, .plate-guide, .plate-review { grid-template-columns: 1fr; }
            .chart-head { flex-direction: column; }
            .hospital-scene { min-height: 310px; }
            .bed { right: 20px; width: 210px; }
            .cross-card { display: none; }
            @keyframes arrive {
                0% { transform: translateX(0); opacity: 0; }
                100% { transform: translateX(230px); opacity: 1; }
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    if hero_background:
        st.markdown(
            f"""
            <style>
            .stApp::before {{
                content: "";
                position: fixed;
                inset: 0;
                pointer-events: none;
                z-index: 0;
                opacity: .16;
                background:
                    radial-gradient(circle at center, rgba(255, 255, 255, .2) 0%, rgba(244, 247, 242, .7) 58%, rgba(244, 247, 242, .94) 100%),
                    url("{hero_background}") center 44% / min(86vw, 980px) auto no-repeat;
            }}
            .block-container {{
                position: relative;
                z-index: 1;
            }}
            @media (max-width: 760px) {{
                .stApp::before {{
                    opacity: .11;
                    background:
                        radial-gradient(circle at center, rgba(255, 255, 255, .2) 0%, rgba(244, 247, 242, .78) 62%, rgba(244, 247, 242, .96) 100%),
                        url("{hero_background}") center 32% / 135vw auto no-repeat;
                }}
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )


def header(title, subtitle="", show_status=True):
    st.markdown(
        f"""
        <div class="top-actions">
            <div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Ver ranking en vivo"):
            go_ranking()
    with col2:
        if st.session_state.screen != "start" and st.button("Nueva partida de este grupo"):
            reset_my_game()
    with col3:
        with st.popover("Info del proyecto"):
            collaborators = "".join(
                [f"<li>{html.escape(name)}</li>" for name in CREDITS["collaborators"]]
            )
            st.markdown(
                f"""
                <div class="credits-box">
                    <h3>Misión Nutrición</h3>
                    <p><strong>Lema:</strong> {html.escape(CREDITS["lema"])}</p>
                    <p><strong>Diseño y edición:</strong> {html.escape(CREDITS["design"])}</p>
                    <p><strong>Colaboradores:</strong></p>
                    <ul>{collaborators}</ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if show_status and st.session_state.screen not in {"start", "ranking"}:
        health = max(0, min(100, st.session_state.patient_health))
        st.markdown(
            f"""
            <div class="status-bar">
                <div class="pill">Grupo: {st.session_state.team_name}</div>
                <div class="pill">Puntaje: {st.session_state.score}</div>
                <div class="pill">Estado del paciente: {health}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def panel_open(title):
    st.markdown(f'<div class="panel"><h2>{title}</h2>', unsafe_allow_html=True)


def panel_close():
    st.markdown("</div>", unsafe_allow_html=True)


def message_box():
    if st.session_state.last_message:
        st.info(st.session_state.last_message)


def patient_figure():
    return (
        '<div class="patient-runner">'
        '<div class="head"></div>'
        '<div class="torso"></div>'
        '<div class="arm-l"></div>'
        '<div class="arm-r"></div>'
        '<div class="leg-l"></div>'
        '<div class="leg-r"></div>'
        "</div>"
    )


def hospital_scene(caption):
    html = (
        '<div class="hospital-scene">'
        '<div class="consult-door"></div>'
        '<div class="bed"></div>'
        '<div class="cross-card"></div>'
        f"{patient_figure()}"
        f'<div class="scene-caption">{caption}</div>'
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def result_scene(status, color):
    html = (
        f'<div class="hospital-scene result-scene" style="--result-color: {color};">'
        f'<div class="monitor">{st.session_state.patient_health}%</div>'
        '<div class="ecg"></div>'
        '<div class="bed"></div>'
        f"{patient_figure()}"
        f'<div class="scene-caption">{status}</div>'
        "</div>"
    )
    st.markdown(html, unsafe_allow_html=True)


def screen_start():
    header(
        "Misión Nutrición",
        "Formulario por pasos: cada grupo entra al mismo link, juega su caso y envía su resultado.",
        False,
    )
    message_box()
    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        panel_open("Ingreso del grupo")
        st.write("Escriban el nombre de su grupo. Cada equipo puede jugar desde su propia computadora o celular.")
        team_name = st.text_input("Nombre del grupo", value=st.session_state.team_name, placeholder="Ejemplo: Grupo 3 - Los Nutris")
        st.markdown(
            """
            <div class="step-list">
                <div class="step">1. Paciente</div>
                <div class="step">2. Diagnóstico</div>
                <div class="step">3. Alimentos</div>
                <div class="step">4. Plato</div>
                <div class="step">5. Carta</div>
                <div class="step">6. Ranking</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        panel_close()
        if st.button("Iniciar mi caso"):
            start_game(team_name)

    with right:
        panel_open("Roles sugeridos")
        st.markdown(
            '<div class="roles">'
            + "".join([f'<div class="role">{role}</div>' for role in ROLES])
            + "</div>",
            unsafe_allow_html=True,
        )
        panel_close()



def screen_arrival():
    patient = current_patient()
    header("Ingreso del paciente", patient["name"])
    hospital_scene("El paciente está llegando a consulta...")
    if st.button("Continuar a historia clínica"):
        set_screen("case")


def screen_case():
    patient = current_patient()
    header("Historia clínica", patient["name"])
    symptoms = "".join(
        [f'<span class="clinical-tag">{symptom}</span>' for symptom in patient["symptoms"]]
    )
    vitals = "".join(
        [
            f'<div class="chart-line"><span>{label}</span><strong>{value}</strong></div>'
            for label, value in patient["vitals"].items()
        ]
    )
    st.markdown(
        f"""
        <div class="chart">
            <div class="chart-head">
                <div>
                    <h2>Expediente nutricional</h2>
                    <p>{patient["name"]}</p>
                </div>
                <div class="chart-id">Admisiones / Caso activo</div>
            </div>
            <div class="chart-grid">
                <div class="chart-section">
                    <h3>Datos de ingreso</h3>
                    <div class="chart-line"><span>Edad</span><strong>{patient["age"]}</strong></div>
                    <div class="chart-line"><span>Motivo</span><strong>{patient["reason"]}</strong></div>
                    <div class="chart-line"><span>Habitos relevantes</span><strong>{patient["habits"]}</strong></div>
                </div>
                <div class="chart-section">
                    <h3>Estado inicial</h3>
                    {vitals}
                </div>
                <div class="chart-section">
                    <h3>Signos observados</h3>
                    <div class="tag-list">{symptoms}</div>
                </div>
                <div class="chart-section">
                    <h3>Nota para el equipo</h3>
                    <p>{patient["case"]}</p>
                    <div class="note">Analicen el caso antes de elegir el diagnóstico. La siguiente pantalla es la primera decisión con puntaje.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Continuar al diagnóstico"):
        set_screen("diagnosis")


def screen_diagnosis():
    patient = current_patient()
    header("Paso 1: Diagnóstico Express", "El equipo debe identificar el problema nutricional más probable.")
    message_box()

    st.markdown(
        f"""
        <div class="mission-alert">
            Caso recibido: {patient["case"]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    options = [
        ("Anemia", "Cansancio, palidez, mareos y posible bajo consumo de hierro."),
        ("Diabetes", "Sed frecuente, cansancio y consumo alto de azúcares simples."),
        ("Obesidad", "Exceso de peso, poca actividad y alta ingesta de comida rápida."),
        ("Hipertensión", "Presión elevada y consumo frecuente de alimentos salados."),
    ]

    st.markdown(
        '<div class="diagnosis-grid">'
        + "".join(
            [
                f'<div class="diagnosis-card"><h3>{name}</h3><p>{hint}</p></div>'
                for name, hint in options
            ]
        )
        + "</div>",
        unsafe_allow_html=True,
    )

    cols = st.columns(4)
    for index, (name, _) in enumerate(options):
        with cols[index]:
            if st.button(f"Elegir {name}", key=f"diagnosis_{name}"):
                choose_diagnosis(name)


def food_details(food):
    lower = food.lower()
    if any(word in lower for word in ["agua", "gaseosa", "vino"]):
        return "Bebida", "&#129380;"
    if any(word in lower for word in ["pollo", "pescado", "huevo", "carne", "hígado", "higado", "pica", "asado"]):
        return "Proteína", "&#127831;"
    if any(word in lower for word in ["avena", "arroz", "pan", "lentejas", "frijoles", "legumbres"]):
        return "Energía y fibra", "&#127806;"
    if any(word in lower for word in ["verduras", "espinaca", "brócoli", "brocoli", "frutas", "manzana", "plátano", "platano", "palta"]):
        return "Frutas y verduras", "&#129382;"
    if any(word in lower for word in ["leche", "queso", "yogur"]):
        return "Lácteo", "&#129371;"
    if any(word in lower for word in ["dulces", "pasteles", "caramelos", "hamburguesa", "fritas", "frituras", "snacks", "sopas"]):
        return "Ultraprocesado", "&#127839;"
    return "Alimento", "&#127858;"


def screen_foods():
    prepare_foods()
    patient = current_patient()
    header("Paso 2: Mercado Saludable", "Arma una canasta con exactamente 3 alimentos recomendados.")
    message_box()
    chosen = [
        food
        for food in st.session_state.food_options
        if st.session_state.get(f"food_{food}", False)
    ]
    slots = chosen[:]
    while len(slots) < 3:
        slots.append("")
    slot_html = "".join(
        [
            f'<div class="basket-slot">{html.escape(food)}</div>'
            if food
            else '<div class="basket-slot empty">Espacio libre</div>'
            for food in slots[:3]
        ]
    )

    market_html = (
        '<div class="market-top">'
        f'<div class="mission-alert">Caso activo: {html.escape(patient["case"])}<br>'
        "Objetivo: elijan 3 productos para ayudar al paciente. Hay opciones trampa mezcladas.</div>"
        '<div class="basket"><h3>Canasta del equipo</h3>'
        f'<div class="basket-count">{len(chosen)} de 3 seleccionados</div>'
        f'<div class="basket-slots">{slot_html}</div></div>'
        "</div>"
    )
    st.markdown(market_html, unsafe_allow_html=True)

    cols = st.columns(4)
    for index, food in enumerate(st.session_state.food_options):
        selected = st.session_state.get(f"food_{food}", False)
        category, icon = food_details(food)
        with cols[index % 4]:
            selected_class = " selected" if selected else ""
            selected_text = "En canasta" if selected else "Disponible"
            card_html = (
                f'<div class="food-card{selected_class}">'
                "<div>"
                f'<div class="food-icon">{icon}</div>'
                f"<h3>{html.escape(food)}</h3>"
                f"<p>{html.escape(category)}</p>"
                "</div>"
                f'<span class="food-status">{selected_text}</span>'
                "</div>"
            )
            st.markdown(card_html, unsafe_allow_html=True)
            action = "Quitar" if selected else "Agregar"
            disabled = not selected and len(chosen) >= 3
            if st.button(f"{action}", key=f"toggle_{food}", disabled=disabled):
                toggle_food(food)
                st.rerun()

    if st.button("Evaluar alimentos"):
        check_foods()


def screen_plate():
    header("Paso 3: Revision del plato", "El sistema revisa la canasta que el equipo eligio en el mercado.")
    message_box()
    patient = current_patient()
    chosen = selected_foods()
    points, title, detail = plate_review()
    food_cards = []
    for food in chosen:
        category, icon = food_details(food)
        is_good = food in patient["foods_good"]
        status = "Recomendado" if is_good else "Revisar"
        css_class = "good" if is_good else "bad"
        food_cards.append(
            f'<div class="review-food {css_class}"><div class="food-icon">{icon}</div>'
            f"<h3>{html.escape(food)}</h3><p>{html.escape(category)}</p>"
            f'<span class="review-badge">{status}</span></div>'
        )

    st.markdown(
        f"""
        <div class="mission-alert">
            Caso activo: {html.escape(patient["case"])}<br>
            Ahora se revisa si la canasta elegida realmente ayuda al paciente.
        </div>
        <div class="plate-guide">
            <div class="plate-part"><strong>Meta</strong><span>Elegir alimentos recomendados para el diagnóstico.</span></div>
            <div class="plate-part"><strong>Canasta</strong><span>{len(chosen)} de 3 alimentos seleccionados.</span></div>
            <div class="plate-part"><strong>Puntaje</strong><span>{title}: +{points} puntos.</span></div>
        </div>
        <div class="plate-review">
            {"".join(food_cards)}
        </div>
        <div class="teacher-panel">
            <h3>{title}</h3>
            <p>{html.escape(detail)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Confirmar revision y tomar carta sorpresa"):
        plate_score(points)


def screen_surprise():
    header("Paso 4: Carta Sorpresa", "Un evento cambia el resultado del paciente.")
    panel_open("Evento")
    st.markdown(f"### {st.session_state.surprise_text}")
    panel_close()
    if st.button("Ver resultado y enviar al ranking"):
        set_screen("result")


def screen_result():
    status, color, detail = classify_result()
    patient = current_patient()
    submit_result_once()
    header("Resultado enviado", "Tu resultado ya fue agregado al ranking en vivo.")
    result_scene(status, color)
    panel_open("Resumen del grupo")
    st.markdown(f"### {status}")
    st.write(detail)
    st.write(f"Grupo: {st.session_state.team_name}")
    st.write(f"Caso: {patient['name']}")
    st.write(f"Puntaje total: {st.session_state.score}")
    st.write(f"Estado del paciente: {st.session_state.patient_health}%")
    st.success(patient["advice"])
    panel_close()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Ver ranking final"):
            go_ranking()
    with col2:
        if st.button("Jugar otro caso"):
            reset_my_game()


def screen_ranking():
    header("Ranking en vivo", "Todos los grupos ven esta misma tabla.", False)
    results = sorted_results()
    if not results:
        st.warning("Todavía no hay resultados enviados.")
    else:
        table_rows = []
        for position, result in enumerate(results, start=1):
            row_class = ' class="rank-first"' if position == 1 else ""
            team = html.escape(str(result.get("team", "")))
            patient = html.escape(str(result.get("patient", "")).replace("Paciente ", "P. "))
            score = html.escape(str(result.get("score", 0)))
            health = html.escape(str(result.get("health", 0)))
            status = html.escape(str(result.get("status", "")))
            submitted_at = html.escape(str(result.get("submitted_at", "")))
            table_rows.append(
                f'<tr{row_class}><td>#{position}</td><td>{team}</td><td>{patient}</td>'
                f'<td class="score-cell">{score}</td><td>{health}%</td><td>{status}</td>'
                f"<td>{submitted_at}</td></tr>"
            )
        table_html = (
            '<div class="ranking-wrap"><table class="ranking-table"><thead><tr>'
            "<th>Puesto</th><th>Grupo</th><th>Paciente</th><th>Puntaje</th>"
            "<th>Estado</th><th>Resultado</th><th>Hora</th>"
            f"</tr></thead><tbody>{''.join(table_rows)}</tbody></table></div>"
        )
        st.markdown(table_html, unsafe_allow_html=True)
        winner = results[0]
        st.success(f"Primer lugar actual: {winner.get('team', '')} con {winner.get('score', 0)} puntos")
        st.download_button(
            "Descargar ranking",
            data=ranking_csv(results),
            file_name=f"ranking_mision_nutricion_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Actualizar ranking"):
            st.rerun()
    with col2:
        if st.button("Volver a mi juego"):
            set_screen(st.session_state.return_screen)


SCREENS = {
    "start": screen_start,
    "arrival": screen_arrival,
    "case": screen_case,
    "diagnosis": screen_diagnosis,
    "foods": screen_foods,
    "plate": screen_plate,
    "surprise": screen_surprise,
    "result": screen_result,
    "ranking": screen_ranking,
}


init_state()
inject_css()
SCREENS[st.session_state.screen]()
