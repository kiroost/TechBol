
from flask import render_template, request, redirect, url_for
from app import db
from app.models import Pedido, Cliente, Producto
from app.pedidos import bp_pedidos
from datetime import date


# Mostrar pedidos
@bp_pedidos.route('/')
def listar():

    pedidos = Pedido.query.all()

    return render_template(
        'listado_pedidos.html',
        pedidos=pedidos
    )


# Registrar pedido
@bp_pedidos.route('/nuevo', methods=['GET', 'POST'])
def nuevo():

    clientes = Cliente.query.all()
    productos = Producto.query.all()

    if request.method == 'POST':

        pedido = Pedido(
            fecha=date.fromisoformat(request.form['fecha']),
            monto=float(request.form['monto']),
            cliente_id=int(request.form['cliente_id']),
            producto_id=int(request.form['producto_id'])
        )

        db.session.add(pedido)
        db.session.commit()

        return redirect(url_for('pedidos.listar'))

    return render_template(
        'formulario_pedido.html',
        clientes=clientes,
        productos=productos
    )


# Editar pedido
@bp_pedidos.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):

    pedido = Pedido.query.get_or_404(id)

    clientes = Cliente.query.all()
    productos = Producto.query.all()

    if request.method == 'POST':

        pedido.fecha = date.fromisoformat(request.form['fecha'])
        pedido.monto = float(request.form['monto'])
        pedido.cliente_id = int(request.form['cliente_id'])
        pedido.producto_id = int(request.form['producto_id'])

        db.session.commit()

        return redirect(url_for('pedidos.listar'))

    return render_template(
        'formulario_pedido.html',
        pedido=pedido,
        clientes=clientes,
        productos=productos
    )


# Eliminar pedido
@bp_pedidos.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):

    pedido = Pedido.query.get_or_404(id)

    db.session.delete(pedido)
    db.session.commit()

    return redirect(url_for('pedidos.listar'))
