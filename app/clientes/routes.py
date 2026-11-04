
from flask import render_template, request, redirect, url_for
from app import db
from app.models import Cliente
from app.clientes import bp_clientes


@bp_clientes.route('/')
def listar():
    clientes = Cliente.query.all()
    return render_template(
        'listado.html',
        titulo='Clientes',
        registros=clientes,
        campos=['nombre', 'telefono'],
        nuevo=url_for('clientes.nuevo'),
        editar='clientes.editar',
        eliminar='clientes.eliminar'
    )


@bp_clientes.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        cliente = Cliente(
            nombre=request.form['nombre'],
            telefono=request.form['telefono']
        )
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('clientes.listar'))

    return render_template(
        'formulario.html',
        titulo='Nuevo cliente',
        campos=['nombre', 'telefono']
    )


@bp_clientes.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cliente = db.get_or_404(Cliente, id)

    if request.method == 'POST':
        cliente.nombre = request.form['nombre']
        cliente.telefono = request.form['telefono']
        db.session.commit()
        return redirect(url_for('clientes.listar'))

    return render_template(
        'formulario.html',
        titulo='Editar cliente',
        campos=['nombre', 'telefono'],
        registro=cliente
    )


@bp_clientes.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    cliente = db.get_or_404(Cliente, id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('clientes.listar'))
