
from flask import render_template, request, redirect, url_for
from app import db
from app.models import Producto
from app.productos import bp_productos


@bp_productos.route('/')
def listar():

    productos = Producto.query.all()

    return render_template(
        'listado.html',
        titulo='Productos',
        registros=productos,
        campos=['nombre', 'precio', 'stock'],
        nuevo=url_for('productos.nuevo'),
        editar='productos.editar',
        eliminar='productos.eliminar'
    )


@bp_productos.route('/nuevo', methods=['GET', 'POST'])
def nuevo():

    if request.method == 'POST':

        producto = Producto(
            nombre=request.form['nombre'],
            precio=float(request.form['precio']),
            stock=int(request.form['stock'])
        )

        db.session.add(producto)
        db.session.commit()

        return redirect(url_for('productos.listar'))

    return render_template(
        'formulario.html',
        titulo='Nuevo producto',
        campos=['nombre', 'precio', 'stock']
    )


@bp_productos.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):

    producto = Producto.query.get_or_404(id)

    if request.method == 'POST':

        producto.nombre = request.form['nombre']
        producto.precio = float(request.form['precio'])
        producto.stock = int(request.form['stock'])

        db.session.commit()

        return redirect(url_for('productos.listar'))

    return render_template(
        'formulario.html',
        titulo='Editar producto',
        campos=['nombre', 'precio', 'stock'],
        registro=producto
    )


@bp_productos.route('/eliminar/<int:id>')
def eliminar(id):

    producto = Producto.query.get_or_404(id)

    db.session.delete(producto)
    db.session.commit()

    return redirect(url_for('productos.listar'))
