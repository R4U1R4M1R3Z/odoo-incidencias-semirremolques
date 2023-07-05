from odoo import api, fields, models, _


class ViaDeteccion(models.Model):
    _name = 'via.deteccion'
    _description = 'Vía de detección'

    name = fields.Char(string='Nombre')


class Categoria(models.Model):
    _name = 'categoria'
    _description = 'Categoría'

    name = fields.Char(string='Nombre')


class Incidencias(models.Model):
    _name = 'incidencias'
    _description = 'Módulo de incidencias'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']

    icon = 'incidencias,static/description/icon.png'


    date = fields.Date(string='Fecha de creación', default=fields.Date.context_today)
    dateFabricacion = fields.Date(string="Fecha de fabricación")
    strDescripcion = fields.Html(string='Descripción',tracking=True)
    strCausa = fields.Html(string='Causa',tracking=True)
    strSolucion = fields.Html(string='Solución',tracking=True)
    state = fields.Selection([
        ('abierta', 'Abierta'),
        ('en_proceso', 'En Proceso'),
        ('resuelta', 'Resuelta'),
        ('cerrada_efectiva', 'Cerrada'),
        ('cancelada', 'Cancelada'),
    ], string='Estado',tracking=True)
    fecha_solucion = fields.Date(string='Fecha de solución',tracking=True)
    name = fields.Char(string='Identificador de incidencia', compute='_compute_name', store=True, readonly=True)
    strNumFurgon = fields.Char(string='Número de furgón',tracking=True)
    strNumChasis = fields.Char(string='Número de chasis',tracking=True)
    strNumMatricula = fields.Char(string='Matrícula',tracking=True)
    cliente_id = fields.Many2one('res.partner', string='Cliente',tracking=True)
    empresa_id = fields.Many2one('res.partner', string='Empresa asignada',tracking=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id.id,tracking=True
    )
    flcoste = fields.Monetary(string='Coste',tracking=True)
    strViaDeteccion = fields.Many2one('via.deteccion', string='Vía de detección',tracking=True)
    tipo = fields.Selection([
        ('poliester', 'Poliéster'),
        ('acabados', 'Acabados'),
        ('chasis', 'Chasis')
    ], string='Tipo de incidencia',tracking=True)
    strCategoria = fields.Many2one('categoria', string='Categoría',tracking=True)
    empleado_id = fields.Many2one('hr.employee', string='Empleado asignado',tracking=True)


    @api.model
    def create(self, vals):
        sequence_obj = self.env['ir.sequence']
        name = sequence_obj.next_by_code('incidencias.sequence') or '/'
        vals['name'] = name
        vals['state'] = 'abierta'
        return super(Incidencias, self).create(vals)

    def preparar(self):
        self.state = 'en_proceso'

    def resolver(self):
        self.state = 'resuelta'

    def cancelar(self):
        self.state = 'cancelada'

    def cerrar(self):
        self.state = 'cerrada_efectiva'

    def abrir_asistente_correo(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'incidencias',
            'default_res_id': self.ids[0],
            'default_use_template': False,  # Aquí desactivamos la plantilla
            'mark_so_as_sent': True,
            'force_email': True
        }
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
