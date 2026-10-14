-- Álbum de los 50 de Gabriela · configuración de Supabase Storage
-- Pégalo completo en Supabase > SQL Editor > New query y presiona "Run".

-- 1) Bucket público "album": máximo 15 MB por foto y solo imágenes
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('album', 'album', true, 15728640,
        array['image/jpeg', 'image/png', 'image/webp', 'image/heic', 'image/heif'])
on conflict (id) do update
  set public = excluded.public,
      file_size_limit = excluded.file_size_limit,
      allowed_mime_types = excluded.allowed_mime_types;

-- 2) Cualquiera con el enlace puede VER y LISTAR las fotos del álbum
create policy "album: ver fotos"
on storage.objects for select
to anon, authenticated
using (bucket_id = 'album');

-- 3) Los invitados solo pueden SUBIR a la carpeta "invitados"
--    (no pueden borrar ni reemplazar fotos, ni subir a "oficial")
create policy "album: invitados suben"
on storage.objects for insert
to anon, authenticated
with check (bucket_id = 'album' and (storage.foldername(name))[1] = 'invitados');

-- La carpeta "oficial" (fotos del fotógrafo) solo la llenas tú:
-- desde el panel de Supabase (Storage > album > oficial) o con subir_fotografo.py.
