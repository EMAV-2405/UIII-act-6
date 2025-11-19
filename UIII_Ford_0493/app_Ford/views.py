from django.shortcuts import render, redirect, get_object_or_404
from .models import Vehiculo, Empleado, Venta, Cliente, Proveedor, ServicioMantenimiento
from datetime import date 


# ==========================================
# VISTA INICIO
# ==========================================
def inicio_ford(request):
    return render(request, 'inicio.html')


# ==========================================
# CRUD VEHICULO
# ==========================================
def agregar_vehiculo(request):
    if request.method == "POST":
        Vehiculo.objects.create(
            marca=request.POST.get('marca'),
            modelo=request.POST.get('modelo'),
            anio=request.POST.get('anio'),
            precio=request.POST.get('precio'),
            cantidad_disponible=request.POST.get('cantidad_disponible'),
            numero_serie=request.POST.get('numero_serie'),
            color=request.POST.get('color')
        )
        return redirect('ver_vehiculos')
    
    return render(request, 'vehiculos/agregar_vehiculo.html')


def ver_vehiculos(request):
    return render(request, 'vehiculos/ver_vehiculos.html', {
        'vehiculos': Vehiculo.objects.all()
    })


def actualizar_vehiculo(request, id):
    vehiculo = get_object_or_404(Vehiculo, id=id)

    if request.method == "POST":
        vehiculo.marca = request.POST.get('marca')
        vehiculo.modelo = request.POST.get('modelo')
        vehiculo.anio = request.POST.get('anio')
        vehiculo.precio = request.POST.get('precio')
        vehiculo.cantidad_disponible = request.POST.get('cantidad_disponible')
        vehiculo.numero_serie = request.POST.get('numero_serie')
        vehiculo.color = request.POST.get('color')
        vehiculo.save()
        return redirect('ver_vehiculos')

    return render(request, 'vehiculos/actualizar_vehiculo.html', {'vehiculo': vehiculo})


def borrar_vehiculo(request, id):
    get_object_or_404(Vehiculo, id=id).delete()
    return redirect('ver_vehiculos')


# ==========================================
# CRUD EMPLEADO
# ==========================================
def agregar_empleado(request):
    if request.method == "POST":
        Empleado.objects.create(
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            puesto=request.POST.get('puesto'),
            telefono=request.POST.get('telefono'),
            email=request.POST.get('email'),
            fecha_contratacion=request.POST.get('fecha_contratacion'),
            salario=request.POST.get('salario')
        )
        return redirect('ver_empleados')

    return render(request, 'empleados/agregar_empleado.html')


def ver_empleados(request):
    return render(request, 'empleados/ver_empleados.html', {
        'empleados': Empleado.objects.all()
    })


def actualizar_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)

    if request.method == "POST":
        empleado.nombre = request.POST.get('nombre')
        empleado.apellido = request.POST.get('apellido')
        empleado.puesto = request.POST.get('puesto')
        empleado.telefono = request.POST.get('telefono')
        empleado.email = request.POST.get('email')
        empleado.fecha_contratacion = request.POST.get('fecha_contratacion')
        empleado.salario = request.POST.get('salario')
        empleado.save()
        return redirect('ver_empleados')

    return render(request, 'empleados/actualizar_empleado.html', {'empleado': empleado})


def borrar_empleado(request, id):
    get_object_or_404(Empleado, id=id).delete()
    return redirect('ver_empleados')


# ==========================================
# CRUD CLIENTE
# ==========================================
def agregar_cliente(request):
    if request.method == "POST":
        Cliente.objects.create(
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            correo_electronico=request.POST.get('correo_electronico'),
            telefono=request.POST.get('telefono')
        )
        return redirect('ver_clientes')

    return render(request, 'clientes/agregar_cliente.html')


def ver_clientes(request):
    return render(request, 'clientes/ver_clientes.html', {
        'clientes': Cliente.objects.all()
    })


def actualizar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == "POST":
        cliente.nombre = request.POST.get('nombre')
        cliente.apellido = request.POST.get('apellido')
        cliente.correo_electronico = request.POST.get('correo_electronico')
        cliente.telefono = request.POST.get('telefono')
        cliente.save()
        return redirect('ver_clientes')

    return render(request, 'clientes/actualizar_cliente.html', {'cliente': cliente})


def borrar_cliente(request, id):
    get_object_or_404(Cliente, id=id).delete()
    return redirect('ver_clientes')


# ==========================================
# CRUD VENTA — COMPLETAMENTE ACTUALIZADO
# ==========================================
def agregar_venta(request):
    contexto = {
        'vehiculos': Vehiculo.objects.all(),
        'empleados': Empleado.objects.all(),
        'clientes': Cliente.objects.all()
    }

    if request.method == "POST":
        vehiculo = get_object_or_404(Vehiculo, id=request.POST.get('vehiculo'))

        # Verificar stock
        if vehiculo.cantidad_disponible <= 0:
            contexto['error'] = "NO HAY STOCK DISPONIBLE."
            return render(request, 'ventas/agregar_venta.html', contexto)

        empleado = get_object_or_404(Empleado, id=request.POST.get('empleado')) if request.POST.get('empleado') else None
        cliente = get_object_or_404(Cliente, id=request.POST.get('cliente'))

        Venta.objects.create(
            vehiculo=vehiculo,
            empleado=empleado,
            cliente=cliente,
            total=request.POST.get('total'),
            metodo_pago=request.POST.get('metodo_pago'),
            folio=request.POST.get('folio'),
            fecha_venta=date.today()
        )

        # Restar stock
        vehiculo.cantidad_disponible -= 1
        vehiculo.save()

        return redirect('ver_ventas')

    return render(request, 'ventas/agregar_venta.html', contexto)



def ver_ventas(request):
    return render(request, 'ventas/ver_ventas.html', {
        'ventas': Venta.objects.select_related('vehiculo', 'empleado', 'cliente').all()
    })



def actualizar_venta(request, id):
    venta = get_object_or_404(Venta, id=id)

    contexto = {
        'venta': venta,
        'vehiculos': Vehiculo.objects.all(),
        'empleados': Empleado.objects.all(),
        'clientes': Cliente.objects.all()
    }

    if request.method == "POST":
        nuevo_vehiculo = get_object_or_404(Vehiculo, id=request.POST.get('vehiculo'))

        # Si cambió el vehículo → actualizar stock
        if venta.vehiculo.id != nuevo_vehiculo.id:

            # Validar stock del nuevo vehículo
            if nuevo_vehiculo.cantidad_disponible <= 0:
                contexto['error'] = "NO hay stock del vehículo nuevo."
                return render(request, 'ventas/actualizar_venta.html', contexto)

            # Regresar el stock del viejo vehículo
            venta.vehiculo.cantidad_disponible += 1
            venta.vehiculo.save()

            # Descontar stock del nuevo
            nuevo_vehiculo.cantidad_disponible -= 1
            nuevo_vehiculo.save()

        # Guardar cambios en la venta
        venta.vehiculo = nuevo_vehiculo
        venta.empleado = get_object_or_404(Empleado, id=request.POST.get('empleado')) if request.POST.get('empleado') else None
        venta.cliente = get_object_or_404(Cliente, id=request.POST.get('cliente'))
        venta.total = request.POST.get('total')
        venta.metodo_pago = request.POST.get('metodo_pago')
        venta.folio = request.POST.get('folio')

        venta.save()
        return redirect('ver_ventas')

    return render(request, 'ventas/actualizar_venta.html', contexto)



def borrar_venta(request, id):
    venta = get_object_or_404(Venta, id=id)

    # Regresar stock
    venta.vehiculo.cantidad_disponible += 1
    venta.vehiculo.save()

    venta.delete()
    return redirect('ver_ventas')



# ==========================================
# CRUD PROVEEDOR
# ==========================================
def agregar_proveedor(request):
    if request.method == "POST":
        Proveedor.objects.create(
            nombre_proveedor=request.POST.get('nombre_proveedor'),
            telefono=request.POST.get('telefono'),
            direccion=request.POST.get('direccion'),
            email=request.POST.get('email'),
            producto=request.POST.get('producto')
        )
        return redirect('ver_proveedores')

    return render(request, 'proveedores/agregar_proveedor.html')


def ver_proveedores(request):
    return render(request, 'proveedores/ver_proveedores.html', {
        'proveedores': Proveedor.objects.all()
    })


def actualizar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)

    if request.method == "POST":
        proveedor.nombre_proveedor = request.POST.get('nombre_proveedor')
        proveedor.telefono = request.POST.get('telefono')
        proveedor.direccion = request.POST.get('direccion')
        proveedor.email = request.POST.get('email')
        proveedor.producto = request.POST.get('producto')
        proveedor.save()
        return redirect('ver_proveedores')

    return render(request, 'proveedores/actualizar_proveedor.html', {'proveedor': proveedor})


def borrar_proveedor(request, id):
    get_object_or_404(Proveedor, id=id).delete()
    return redirect('ver_proveedores')



# ==========================================
# CRUD SERVICIO MANTENIMIENTO
# ==========================================
def agregar_servicio(request):
    contexto = {
        'vehiculos': Vehiculo.objects.all(),
        'clientes': Cliente.objects.all(),
        'proveedores': Proveedor.objects.all()
    }

    if request.method == "POST":
        ServicioMantenimiento.objects.create(
            vehiculo=get_object_or_404(Vehiculo, id=request.POST.get('vehiculo')),
            cliente=get_object_or_404(Cliente, id=request.POST.get('cliente')),
            proveedor=get_object_or_404(Proveedor, id=request.POST.get('proveedor')),
            tipo_servicio=request.POST.get('tipo_servicio'),
            fecha_servicio=request.POST.get('fecha_servicio'),
            costo_servicio=request.POST.get('costo_servicio')
        )
        return redirect('ver_servicios')

    return render(request, 'servicios/agregar_servicio.html', contexto)


def ver_servicios(request):
    return render(request, 'servicios/ver_servicios.html', {
        'servicios': ServicioMantenimiento.objects.select_related('vehiculo', 'cliente', 'proveedor').all()
    })


def actualizar_servicio(request, id):
    servicio = get_object_or_404(ServicioMantenimiento, id=id)

    contexto = {
        'servicio': servicio,
        'vehiculos': Vehiculo.objects.all(),
        'clientes': Cliente.objects.all(),
        'proveedores': Proveedor.objects.all()
    }

    if request.method == "POST":
        servicio.vehiculo = get_object_or_404(Vehiculo, id=request.POST.get('vehiculo'))
        servicio.cliente = get_object_or_404(Cliente, id=request.POST.get('cliente'))
        servicio.proveedor = get_object_or_404(Proveedor, id=request.POST.get('proveedor'))
        servicio.tipo_servicio = request.POST.get('tipo_servicio')
        servicio.fecha_servicio = request.POST.get('fecha_servicio')
        servicio.costo_servicio = request.POST.get('costo_servicio')
        servicio.save()
        return redirect('ver_servicios')

    return render(request, 'servicios/actualizar_servicio.html', contexto)


def borrar_servicio(request, id):
    get_object_or_404(ServicioMantenimiento, id=id).delete()
    return redirect('ver_servicios')
