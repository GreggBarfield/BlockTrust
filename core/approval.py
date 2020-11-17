import json
from time import time
import uuid
import os
from config import *
from math import sqrt

class Approval:

    # Does NOT support multiple approval at the same time

    def __init__(self, sql):
        self._sql = sql

    def get(self):
        self._sql.execute("""
            SELECT COUNT(*) FROM images 
            WHERE approval='?'
        """)

        remaining_images = self._sql.fetchall()[0][0]

        cols = [
            "id",
            "original_name",
            "original_type",
            "original_password",
            "new_password",
            "new_type",
            "created",
            "original_size_bytes",
            "new_size_bytes",
            "approval"
        ]

        self._sql.execute("""
            SELECT """ + ', '.join(cols) + """
            FROM images 
            WHERE approval='?'
            ORDER BY created ASC
            LIMIT 10
        """)

        return remaining_images, [
            {
                col: row[col_i]
                for col_i, col in enumerate(cols)
            }
            for row in self._sql.fetchall()
        ]

    def decision(self, i, d):
        self._sql.execute("""
            SELECT id, approval
            FROM images 
            WHERE id=%s
        """, (i,))

        f = self._sql.fetchall()

        if len(f) != 1:
            return "Error: Couldn't find row"
        elif f[0][1] != '?':
            return "Error: row already decided"
        elif f[0][0] != int(i):
            return "Error: i not found in " + str(f[0][0])
        
        self._sql.execute("""
            UPDATE images
            SET approval=%s 
            WHERE id=%s
        """, (d, i))

        return False

