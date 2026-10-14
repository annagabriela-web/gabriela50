# Invitación · 50 de Gabriela

Sitio estático para GitHub Pages con álbum compartido (Supabase Storage).

| Archivo | Para qué |
|---|---|
| `index.html` | La invitación completa (imágenes y librería de zip incluidas) |
| `og.jpg` | Vista previa al compartir el enlace por WhatsApp |
| `.nojekyll` | Evita que GitHub procese el sitio |
| `supabase_setup.sql` | Crea el bucket `album` y sus permisos |
| `subir_fotografo.py` | Sube las fotos del fotógrafo a la carpeta `oficial` |

## 1. Publicar en GitHub Pages (10 min)

1. En GitHub (cuenta `annagabriela-web`) crea un repo público llamado **`gabriela50`**.
2. Sube `index.html`, `og.jpg` y `.nojekyll` a la raíz (los otros dos archivos no hace falta subirlos).
3. Settings > Pages > Source: **Deploy from a branch** · Branch: `main` / `(root)` > Save.
4. En 1 o 2 minutos queda en: `https://annagabriela-web.github.io/gabriela50/`

Si usas otro nombre de repo, avísale a Claude para regenerar los enlaces personalizados y la vista previa.

## 2. Crear el álbum en Supabase (5 min)

1. Entra a supabase.com, crea una cuenta y un proyecto nuevo (región: São Paulo o US East).
2. SQL Editor > New query > pega `supabase_setup.sql` > Run.
3. Project Settings > API Keys: copia
   - la **Project URL** (`https://xxxx.supabase.co`)
   - la **publishable key** (`sb_publishable_...`, o la `anon` si tu proyecto usa claves antiguas).
4. Pásale esos 2 datos a Claude y te devuelve el `index.html` con el álbum activado.
   (Son datos públicos por diseño: los permisos del paso 2 limitan lo que se puede hacer.)

Nunca pongas la **secret key** (`sb_secret_...` o `service_role`) en la invitación.

## 3. Cómo funciona el álbum

- **Invitados:** suben fotos desde el celular, sin crear cuenta. Se comprimen a 2048 px antes de subir.
  Solo pueden subir a `invitados/`; no pueden borrar ni reemplazar.
- **Fotógrafo:** solo tú subes a `oficial/`, de dos formas:
  - Panel de Supabase > Storage > album > crea la carpeta `oficial` y arrastra las fotos (redúcelas antes).
  - `python subir_fotografo.py "carpeta"` (reduce a 2400 px y sube; usa la secret key solo en tu compu).
- **Descargas:** cada foto tiene botón "Descargar"; "Descargar todas" baja un .zip de la pestaña abierta.
- **Moderar:** para quitar una foto, bórrala en Storage > album > invitados.
  El nombre del archivo incluye el nombre del invitado que la subió (si entró con su enlace personal).

## Límites del plan gratis de Supabase

- 1 GB de almacenamiento: unas 2,000 fotos de invitados comprimidas, o unas 600 a 900 del fotógrafo a 2400 px.
- Los proyectos gratis se pausan tras 7 días sin actividad; si pasa, entra al panel y presiona "Restore".
