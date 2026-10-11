# Cuentas, Contraseñas y Autenticación Multifactor (MFA) — NubeSoft IT Support

Versión 4.1 · Responsable: IT Support & Security

## 1. Identidad única (SSO)

Todas las aplicaciones corporativas se acceden mediante inicio de sesión único (SSO) con Okta. El usuario es la dirección de correo corporativa (nombre.apellido@nubesoft.com). Las aplicaciones que no admiten SSO se gestionan con el gestor de contraseñas corporativo "1Password Business".

## 2. Requisitos de contraseña

La contraseña de Okta debe cumplir:

- Mínimo 14 caracteres.
- No contener el nombre, el apellido ni el usuario.
- No haber sido usada en las últimas 10 contraseñas.
- No figurar en listas públicas de contraseñas filtradas (Okta lo verifica automáticamente).

La contraseña vence cada 180 días. Se recomienda usar una frase de contraseña de 4 o más palabras. Está prohibido reutilizar la contraseña corporativa en servicios personales.

## 3. Cómo restablecer la contraseña

1. Ir a login.nubesoft.com y hacer clic en "¿Olvidaste tu contraseña?".
2. Ingresar el correo corporativo.
3. Aprobar la verificación en Okta Verify o con el código SMS de respaldo.
4. Elegir una nueva contraseña que cumpla los requisitos.

Si no se tiene acceso al teléfono con Okta Verify, hay que contactar a IT Support por el chat de soporte de la página de inicio de sesión (no requiere autenticación) o llamar a la mesa de ayuda al +54 11 5555-0100 (interno 4357, "HELP"). IT verificará la identidad mediante una videollamada con el documento de identidad antes de restablecer el acceso.

## 4. Bloqueo de cuenta

La cuenta se bloquea durante 30 minutos después de 5 intentos fallidos de inicio de sesión. Pasado ese tiempo se desbloquea sola. Si se necesita acceso urgente, IT Support puede desbloquearla luego de verificar la identidad.

## 5. Autenticación multifactor (MFA)

El MFA es obligatorio para todas las cuentas. Métodos admitidos, en orden de preferencia:

1. Llave de seguridad física FIDO2 (YubiKey). Obligatoria para personas con acceso a producción, a datos de clientes o a sistemas financieros.
2. Okta Verify con notificación push y verificación de número.
3. Código de un solo uso (TOTP) en Okta Verify.

El SMS solo se acepta como método de recuperación, no como método principal.

## 6. Cambio o pérdida del teléfono

Al cambiar de teléfono hay que transferir Okta Verify antes de formatear el teléfono anterior: en el teléfono nuevo, instalar Okta Verify; luego, en login.nubesoft.com > Configuración > "Métodos de verificación", agregar el nuevo dispositivo y eliminar el viejo.

Si el teléfono se perdió o fue robado, hay que avisar a IT Support de inmediato para revocar el factor MFA asociado. Si el teléfono tenía acceso al correo o a Slack corporativo, IT también ejecuta un borrado remoto de los datos corporativos del dispositivo.

## 7. Llaves de seguridad (YubiKey)

Las llaves YubiKey se solicitan en el portal de IT ("Solicitud de hardware > Llave de seguridad"). Cada persona con acceso privilegiado recibe dos llaves: una principal y una de respaldo, que debe guardarse en un lugar seguro distinto. La pérdida de una llave debe reportarse en el día.

## 8. Cuentas compartidas y de servicio

Están prohibidas las cuentas compartidas entre personas. Las cuentas de servicio (para integraciones y automatizaciones) se solicitan al equipo de Plataforma con un ticket, tienen una persona responsable asignada y sus credenciales se guardan en el gestor de secretos "Vault". Nunca deben guardarse secretos, API keys o contraseñas en el código fuente, en Slack ni en documentos compartidos.

## 9. Altas, bajas y cambios de accesos

- Altas: las cuentas de nuevos ingresos se crean automáticamente cuando RR. HH. registra el ingreso en PeopleHub, 3 días hábiles antes de la fecha de inicio.
- Cambios de rol: los accesos a herramientas se piden en el portal de IT ("Solicitud de acceso") y requieren aprobación de la persona líder y, para herramientas sensibles, del dueño de la aplicación.
- Bajas: todos los accesos se desactivan a las 18:00 del último día laboral.
- Revisión de accesos: cada trimestre los líderes deben revisar y confirmar los accesos de su equipo. Los accesos no confirmados en 10 días hábiles se revocan.
