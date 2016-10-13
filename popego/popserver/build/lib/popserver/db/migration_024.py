""" Datos """

__docformat__ = "restructuredtext"

# Se agrega orden a los grupos
# TODO 
#  Agregar StoredProcedure para inicializar las posiciones de cada grupo.
#  Poner como PRIMARY KEY a los 3 campos de itemgroups_items
# Se puede hacer en otra migracion

migration = [
    ("""\
         ALTER TABLE itemgroups_items ADD COLUMN position INTEGER;
         ALTER TABLE itemgroups_items DROP CONSTRAINT itemgroups_items_fk; 
         ALTER TABLE itemgroups_items ADD CONSTRAINT itemgroups_items_fk FOREIGN KEY(itemgroups_id) 
            REFERENCES itemgroups (id) ON DELETE cascade; 
          
      """,
    """\
         ALTER TABLE itemgroups_items DROP CONSTRAINT itemgroups_items_fk; 
         ALTER TABLE itemgroups_items ADD CONSTRAINT itemgroups_items_fk FOREIGN KEY(itemgroups_id) 
            REFERENCES itemgroups (id); 
         ALTER TABLE itemgroups_items DROP COLUMN position;
    """),
]
