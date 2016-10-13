# -*- coding: utf-8 -*-
__docformat__='restructuredtext'

# Migration number: 051
# Interest Cluster Nested Set Tables

migration = [
    ("""
        CREATE TABLE interest_cluster_nested_set (
          id SERIAL NOT NULL,
          lft INTEGER,
          rgt INTEGER,
          PRIMARY KEY (id)
        );

        CREATE TABLE node_interests (
          tags_id integer NOT NULL,
          interest_cluster_nested_set_id integer NOT NULL,
          CONSTRAINT node_interests_tag_id_fk FOREIGN KEY (tags_id) REFERENCES tags(id) ON DELETE CASCADE,
          CONSTRAINT node_interests_icns_id_fk FOREIGN KEY (interest_cluster_nested_set_id) 
            REFERENCES interest_cluster_nested_set(id) ON DELETE CASCADE
        );

        CREATE TABLE node_central_interests (
          tags_id integer NOT NULL,
          interest_cluster_nested_set_id integer NOT NULL,
          CONSTRAINT node_interests_tag_id_fk FOREIGN KEY (tags_id) REFERENCES tags(id) ON DELETE CASCADE,
          CONSTRAINT node_interests_icns_id_fk FOREIGN KEY (interest_cluster_nested_set_id) 
            REFERENCES interest_cluster_nested_set(id) ON DELETE CASCADE

        );


     """, 
     """
        DROP TABLE node_central_interests;
        DROP TABLE node_interests;
        DROP TABLE interest_cluster_nested_set;
     """),
]

