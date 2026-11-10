"""
Formularios y FormSets personalizados para validaciones en el Admin de Django.
"""
from django import forms
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import (
    FaseCaso,
    FaseCartaOpcion,
    Usuario,
    Carta,
    Nivel,
    Mundo,
    EstadoEntidadChoices,
    DificultadChoices,
)


NORMA_ISO_CHOICES = [
    ('ISO/IEC 27001:2022', 'ISO/IEC 27001:2022'),
    ('ISO/IEC 27017', 'ISO/IEC 27017'),
    ('ISO/IEC 20000-1', 'ISO/IEC 20000-1'),
    ('ISO 22301', 'ISO 22301'),
    ('ISO 27001', 'ISO 27001'),
    ('ISO 27701', 'ISO 27701'),
    ('ISO 9001', 'ISO 9001'),
    ('ISO 14001', 'ISO 14001'),
    ('ISO 37301', 'ISO 37301'),
    ('ISO 31000', 'ISO 31000'),
]

AMENAZAS_SUGERIDAS = [
    'Phishing',
    'Fuga de Datos',
    'Acceso No Autorizado',
    'Ingeniería Social',
    'Malware / Ransomware',
    'Elevación de Privilegios',
    'Ataque de Fuerza Bruta',
    'Denegación de Servicio (DoS)',
    'Inyección SQL',
    'Credenciales Comprometidas',
    'Suplantación de Identidad',
    'Incumplimiento Normativo',
]


class CartaForm(forms.ModelForm):
    """
    Formulario estético y validado para la creación y edición de Cartas de Control ISO.
    """
    norma_iso = forms.ChoiceField(
        choices=NORMA_ISO_CHOICES,
        widget=forms.Select(attrs={'class': 'iq-select-custom', 'id': 'id_norma_iso'}),
        label="Norma ISO *"
    )

    class Meta:
        model = Carta
        fields = ['nombre', 'norma_iso', 'concepto', 'descripcion', 'fuerza', 'defensa', 'estado', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'iq-input-custom',
                'id': 'id_nombre',
                'placeholder': 'Ej. Firewall Protector',
                'maxlength': '100',
                'required': 'required',
            }),
            'concepto': forms.TextInput(attrs={
                'class': 'iq-input-custom',
                'id': 'id_concepto',
                'placeholder': 'Ej. Seguridad de la Información',
                'maxlength': '150',
                'required': 'required',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'iq-textarea-custom',
                'id': 'id_descripcion',
                'placeholder': 'Describe el efecto o utilidad de esta carta...',
                'maxlength': '250',
                'rows': 3,
                'required': 'required',
            }),
            'fuerza': forms.NumberInput(attrs={
                'class': 'iq-number-custom',
                'id': 'id_fuerza',
                'min': '0',
                'max': '100',
                'required': 'required',
            }),
            'defensa': forms.NumberInput(attrs={
                'class': 'iq-number-custom',
                'id': 'id_defensa',
                'min': '0',
                'max': '100',
                'required': 'required',
            }),
            'estado': forms.Select(attrs={
                'class': 'iq-select-custom',
                'id': 'id_estado',
            }),
            'imagen': forms.FileInput(attrs={
                'id': 'id_imagen',
                'accept': 'image/jpeg,image/png,image/webp',
            }),
        }


class FaseCartaOpcionInlineFormSet(BaseInlineFormSet):
    """
    Formset con validación estricta de la regla de negocio:
    Máximo 5 cartas por cada FaseCaso.
    """
    def clean(self):
        super().clean()
        if any(self.errors):
            return

        total_cartas = 0
        cartas_seleccionadas = set()

        for form in self.forms:
            # Ignorar formularios marcados para eliminación
            if self.can_delete and self._should_delete_form(form):
                continue

            # Revisar si el formulario tiene datos válidos de carta
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                carta = form.cleaned_data.get('carta')
                if carta:
                    if carta.id in cartas_seleccionadas:
                        raise ValidationError(
                            f"La carta '{carta.nombre}' está duplicada en esta fase. Cada carta debe ser única por fase."
                        )
                    cartas_seleccionadas.add(carta.id)
                    total_cartas += 1

        if total_cartas > 5:
            raise ValidationError(
                f"Regla de negocio infringida: Una fase de caso no puede contener más de 5 cartas asignadas "
                f"(has seleccionado {total_cartas} cartas). Por favor, deja un máximo de 5."
            )


class ReiniciarProgresoForm(forms.Form):
    """
    Formulario de confirmación administrativa para reiniciar progreso de usuarios.
    """
    confirmacion = forms.BooleanField(
        required=True,
        label="Confirmo que deseo reiniciar el progreso (Nivel 1, 0 XP, 0 Oro, 0 Gemas, 3 Vidas)",
        help_text="Esta acción quedará registrada permanentemente en la bitácora de auditoría."
    )
    motivo = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Ej. Reinicio por inicio de ciclo de capacitación anual 2026'}),
        label="Motivo del Reinicio (Opcional para auditoría)"
    )


class FaseCasoForm(forms.ModelForm):
    """
    Formulario visual e interactivo para Crear y Editar Fases de Casos / Incidentes ISO QUEST.
    Soporta live-preview, contador de caracteres y validaciones de unicidad.
    """
    amenaza = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'iq-input-custom',
            'id': 'id_amenaza',
            'placeholder': 'Ej. Phishing',
            'required': 'required',
        }),
        label="Amenaza *"
    )

    class Meta:
        model = FaseCaso
        fields = [
            'nivel',
            'numero_fase',
            'titulo_incidente',
            'amenaza',
            'dificultad',
            'caso_contexto',
            'recompensa_oro',
            'recompensa_xp',
            'estado',
        ]
        widgets = {
            'nivel': forms.Select(attrs={
                'class': 'iq-select-custom',
                'id': 'id_nivel',
                'required': 'required',
            }),
            'numero_fase': forms.NumberInput(attrs={
                'class': 'iq-number-input',
                'id': 'id_numero_fase',
                'min': '1',
                'value': '1',
                'required': 'required',
            }),
            'titulo_incidente': forms.TextInput(attrs={
                'class': 'iq-input-custom',
                'id': 'id_titulo_incidente',
                'placeholder': 'Ej. Acceso No Autorizado',
                'maxlength': '150',
                'required': 'required',
            }),
            'dificultad': forms.Select(attrs={
                'class': 'iq-select-custom',
                'id': 'id_dificultad',
                'required': 'required',
            }),
            'caso_contexto': forms.Textarea(attrs={
                'class': 'iq-textarea-custom',
                'id': 'id_caso_contexto',
                'placeholder': 'Un empleado recibe un correo sospechoso con un enlace para "actualizar su cuenta". ¿Qué debe hacer?',
                'maxlength': '500',
                'rows': 4,
                'required': 'required',
            }),
            'recompensa_oro': forms.NumberInput(attrs={
                'class': 'iq-number-input',
                'id': 'id_recompensa_oro',
                'min': '0',
                'value': '10',
                'required': 'required',
            }),
            'recompensa_xp': forms.NumberInput(attrs={
                'class': 'iq-number-input',
                'id': 'id_recompensa_xp',
                'min': '0',
                'value': '20',
                'required': 'required',
            }),
            'estado': forms.Select(attrs={
                'class': 'iq-select-custom',
                'id': 'id_estado',
            }),
        }

