
import trimesh
import tetgen
import meshio
import pyvista as pv

def stl_to_off(stl_file,off_file):
    """
    Convertit un fichier STL en fichier OFF.
    stl_file: Chemin du fichier STL d'entree.
    off_file: Chemin du fichier OFF de sortie.
    """
    # Charger le fichier STL avec Trimesh
    surface_mesh = trimesh.load_mesh(stl_file)
    
    # V�rifier si c'est bien un maillage triangulaire
    if not isinstance(surface_mesh, trimesh.Trimesh):
        raise ValueError("Le fichier STL n'est pas valide ou n'est pas un maillage triangulaire.")
    else:
        # Export au format off avec x digits sur les floats
        off_content = trimesh.exchange.off.export_off(surface_mesh, digits=5)
        # �crire le contenu dans le fichier
        with open(off_file, 'w') as file:
            file.write(off_content)

# def stl_to_tet(stl_file,tet_file):
#     """
#     Convertit un fichier STL en fichier TET (maillage volumetrique).
#     stl_file: Chemin du fichier STL d'entree.
#     tet_file: Chemin du fichier TET de sortie.
#     """
#     # Charger le fichier STL avec trimesh
#     surface_mesh = trimesh.load(stl_file)
#     if not surface_mesh.is_watertight:
#         raise ValueError("Le maillage STL n'est pas ferme (watertight). Reparez-le avant la conversion.")
    
#     # Convertir le maillage Trimesh en maillage PyVista (PolyData)
#     vertices = surface_mesh.vertices
#     faces = surface_mesh.faces.reshape(-1, 4)[:, 1:]  # Trimesh stocke les faces avec un pr�fixe
#     pv_mesh = pv.PolyData(vertices, faces)
    
#     # V�rifier si le maillage est triangulaire, sinon le trianguler
#     if not pv_mesh.is_all_triangles:
#         pv_mesh = pv_mesh.triangulate()

#     # Passer � TetGen pour la t�trah�dralisation
#     tet = tetgen.TetGen(pv_mesh)
#     tet.tetrahedralize(order=1)  # Ordre 1 : t�tra�dres simples
    
#     # Sauvegarder les fichiers g�n�r�s
#     tet.write_tetgen_files(tet_file)
#     print(f"Tetrahedralisation terminee. Fichiers generes : {tet_file}")


def stl_to_node_ele(stl_file, node_file, ele_file):
    """
    Convertit un fichier STL en fichiers .node et .ele.

    Args:
        stl_file (str): Chemin vers le fichier STL en entree.
        node_file (str): Chemin vers le fichier .node en sortie.
        ele_file (str): Chemin vers le fichier .ele en sortie.
    """
    # Charger le fichier STL avec PyVista
    stl_mesh = pv.read(stl_file)

    # V�rifier que le maillage est triangulaire
    if not stl_mesh.is_all_triangles:
        stl_mesh = stl_mesh.triangulate()

    # T�tra�dralisation avec TetGen
    tet = tetgen.TetGen(stl_mesh)
    tet.tetrahedralize(order=1)

    # Extraire les sommets et les t�tra�dres
    vertices = tet.grid.points
    tets = tet.grid.cells_dict[10]  # 10 est le type de cellule pour les t�tra�dres

    # �crire le fichier .node
    with open(node_file, 'w') as f:
        # Premi�re ligne : nombre de sommets, dimensions, et autres param�tres
        f.write(f"{len(vertices)} 3 0 0\n")
        # �crire les coordonn�es des sommets
        for i, (x, y, z) in enumerate(vertices):
            f.write(f"{i} {x} {y} {z}\n")

    # �crire le fichier .ele
    with open(ele_file, 'w') as f:
        # Premi�re ligne : nombre d'�l�ments, sommets par �l�ment, et autres param�tres
        f.write(f"{len(tets)} 4 0\n")
        # �crire les t�tra�dres
        for i, tet in enumerate(tets):
            f.write(f"{i} {' '.join(map(str, tet))}\n")

    print(f"Fichiers generes : {node_file}, {ele_file}")



def mesh_to_tet(node_file, ele_file, output_tet_file):
    """
    Convertit des fichiers .node et .ele en un fichier .tet au format demande.
  
        node_file (str): Chemin vers le fichier .node contenant les sommets.
        ele_file (str): Chemin vers le fichier .ele contenant les elements.
        output_tet_file (str): Chemin vers le fichier de sortie .tet.
    """
    with open(node_file, 'r') as f:
        lines = f.readlines()
        # Lire le nombre de sommets depuis la premi�re ligne
        num_nodes = int(lines[0].split()[0])
        nodes = []
        for line in lines[1:num_nodes + 1]:
            parts = line.split()
            if len(parts) >= 4:  # ID + x, y, z
                x, y, z = map(float, parts[1:4])  # Ignorer l'ID
                nodes.append((x, y, z))
    
    # Lecture du fichier .ele
    with open(ele_file, 'r') as f:
        lines = f.readlines()
        num_elements = int(lines[0].split()[0])  # Nombre d'�l�ments
        elements = []
        for line in lines[1:num_elements + 1]:
            parts = line.split()
            if len(parts) >= 5:  # ID + 4 vertex indices
                vertex_indices = list(map(int, parts[1:5]))
                elements.append(vertex_indices)
    
    # Cr�ation du fichier .tet
    with open(output_tet_file, 'w') as f:
        # �criture du nombre de sommets et de t�tra�dres
        f.write(f"{len(nodes)} vertices\n")
        f.write(f"{len(elements)} tets\n")
        
        # �criture des sommets
        for node in nodes:
            f.write(f"{node[0]} {node[1]} {node[2]}\n")
        
        # �criture des t�tra�dres (avec '4' au d�but)
        for element in elements:
            f.write(f"4 {' '.join(map(str, element))}\n")
    
    print(f"Fichier .tet cree avec succes : {output_tet_file}")

def off_to_node_ele(off_file, node_file, ele_file):
    mesh = pv.read(off_file)

    # Convertir en PolyData si n�cessaire
    if not isinstance(mesh, pv.PolyData):
        mesh = mesh.extract_surface()

    if not mesh.is_all_triangles:
        mesh = mesh.triangulate()

    tet = tetgen.TetGen(mesh)

    # T�tra�dralisation aved options sp�cifi�es (switches)
    tet.tetrahedralize(order=1)

    # Export fichiers .node et .ele
    vertices = tet.grid.points
    tets = tet.grid.cells_dict[10]

    with open(node_file, 'w') as f:
        f.write(f"{len(vertices)} 3 0 0\n")
        for i, (x, y, z) in enumerate(vertices):
            f.write(f"{i} {x} {y} {z}\n")
        print("Fichier node cree")

    with open(ele_file, 'w') as f:
        f.write(f"{len(tets)} 4 0\n")
        for i, tet in enumerate(tets):
            f.write(f"{i} {' '.join(map(str, tet))}\n")
        print("Fichier ele cree")


