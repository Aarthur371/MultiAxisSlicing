import tetgen
import trimesh

def stl_to_tet(stl_file, tet_file):
    """
    Convertit un fichier STL en fichier TET.
    stl_file: Chemin du fichier STL d'entr�e.
    tet_file: Chemin du fichier TET de sortie.
    """
    # Charger le fichier STL avec Trimesh
    surface_mesh = trimesh.load_mesh(stl_file)
    
    # V�rifier si c'est bien un maillage triangulaire
    if not isinstance(surface_mesh, trimesh.Trimesh):
        raise ValueError("Le fichier STL n'est pas valide ou n'est pas un maillage triangulaire.")
    
    # G�n�rer le maillage volum�trique avec TetGen
    tgen = tetgen.TetGen(surface_mesh)
    nodes, elements = tgen.tetrahedralize(order=1)
    
    # �crire le fichier au format .tet
    with open(tet_file, 'w') as f:
        # �crire le nombre de sommets
        f.write(f"{len(nodes)}\n")
        for node in nodes:
            f.write(f"{node[0]} {node[1]} {node[2]}\n")
        
        # �crire le nombre de t�tra�dres
        f.write(f"{len(elements)}\n")
        for element in elements:
            f.write(f"{element[0]} {element[1]} {element[2]} {element[3]}\n")
    
    print(f"Fichier .tet g�n�r� : {tet_file}")

# Exemple d'utilisation
stl_file = "input\\pyramide1.stl"
tet_file = "output\\pyramide1.tet"
stl_to_tet(stl_file, tet_file)

