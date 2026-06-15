from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# =====================================
# LÓGICA DE TAREAS (Etapa 1)
# =====================================

tareas = []


def agregar_tarea(lista, titulo, descripcion):
    nuevo_id = 1 if not lista else lista[-1]["id"] + 1

    tarea = {
        "id": nuevo_id,
        "titulo": titulo,
        "descripcion": descripcion,
        "completada": False
    }

    lista.append(tarea)


def listar_tareas(lista):
    return lista


def completar_tarea(lista, id):
    for tarea in lista:
        if tarea["id"] == id:
            tarea["completada"] = True
            return True
    return False


def eliminar_tarea(lista, id):
    for tarea in lista:
        if tarea["id"] == id:
            lista.remove(tarea)
            return True
    return False


def filtrar_por_estado(lista, completada):
    return [t for t in lista if t["completada"] == completada]


# =====================================
# RUTAS FLASK
# =====================================

@app.route("/")
def index():

    estado = request.args.get("estado")

    if estado == "completadas":
        lista_mostrar = filtrar_por_estado(tareas, True)

    elif estado == "pendientes":
        lista_mostrar = filtrar_por_estado(tareas, False)

    else:
        lista_mostrar = listar_tareas(tareas)

    return render_template(
        "index.html",
        tareas=lista_mostrar,
        estado=estado
    )


@app.route("/nueva", methods=["GET"])
def nueva_tarea():
    return render_template("nueva_tarea.html")


@app.route("/nueva", methods=["POST"])
def guardar_tarea():

    titulo = request.form["titulo"]
    descripcion = request.form["descripcion"]

    agregar_tarea(
        tareas,
        titulo,
        descripcion
    )

    return redirect(url_for("index"))


@app.route("/completar/<int:id>", methods=["POST"])
def completar(id):

    completar_tarea(tareas, id)

    return redirect(url_for("index"))


@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):

    eliminar_tarea(tareas, id)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)