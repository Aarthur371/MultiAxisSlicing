import os
import trimesh
import tetgen
import meshio
import pyvista as pv

def preprocessing(stl_file,tet_file):
    off_file = "preprocessing//output//" + os.path.splitext(os.path.basename(stl_file))[0] + ".off"
    stl_to_off(stl_file,off_file)
    node_file = "preprocessing//output//" + os.path.splitext(os.path.basename(stl_file))[0] + ".node"
    ele_file = "preprocessing//output//" + os.path.splitext(os.path.basename(stl_file))[0] + ".ele"
    off_to_node_ele(off_file,node_file,ele_file)
    mesh_to_tet(node_file,ele_file,tet_file)

def stl_to_off(stl_file,off_file):
    """
    Convertit un fichier STL en fichier OFF.
    stl_file: Chemin du fichier STL d'entree.
    off_file: Chemin du fichier OFF de sortie.
    """
    # Charger le fichier STL avec Trimesh
    surface_mesh = trimesh.load_mesh(stl_file)
    
    # Vérifier si c'est bien un maillage triangulaire
    if not isinstance(surface_mesh, trimesh.Trimesh):
        raise ValueError("Le fichier STL n'est pas valide ou n'est pas un maillage triangulaire.")
    else:
        # Export au format off avec x digits sur les floats
        off_content = trimesh.exchange.off.export_off(surface_mesh, digits=5)
        # Écrire le contenu dans le fichier
        with open(off_file, 'w') as file:
            file.write(off_content)


def mesh_to_tet(node_file, ele_file, output_tet_file):
    """
    Convertit des fichiers .node et .ele en un fichier .tet au format demande.
  
        node_file (str): Chemin vers le fichier .node contenant les sommets.
        ele_file (str): Chemin vers le fichier .ele contenant les elements.
        output_tet_file (str): Chemin vers le fichier de sortie .tet.
    """
    with open(node_file, 'r') as f:
        lines = f.readlines()
        # Lire le nombre de sommets depuis la première ligne
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
        num_elements = int(lines[0].split()[0])  # Nombre d'éléments
        elements = []
        for line in lines[1:num_elements + 1]:
            parts = line.split()
            if len(parts) >= 5:  # ID + 4 vertex indices
                vertex_indices = list(map(int, parts[1:5]))
                elements.append(vertex_indices)
    
    # Création du fichier .tet
    with open(output_tet_file, 'w') as f:
        # Écriture du nombre de sommets et de tétraèdres
        f.write(f"{len(nodes)} vertices\n")
        f.write(f"{len(elements)} tets\n")
        
        # Écriture des sommets
        for node in nodes:
            f.write(f"{node[0]} {node[1]} {node[2]}\n")
        
        # Écriture des tétraèdres (avec '4' au début)
        for element in elements:
            f.write(f"4 {' '.join(map(str, element))}\n")
    
    print(f"Fichier .tet cree avec succes : {output_tet_file}")

def off_to_node_ele(off_file, node_file, ele_file):
    mesh = pv.read(off_file)

    # Convertir en PolyData si nécessaire
    if not isinstance(mesh, pv.PolyData):
        mesh = mesh.extract_surface()

    if not mesh.is_all_triangles:
        mesh = mesh.triangulate()

    tet = tetgen.TetGen(mesh)

    # Tétraédralisation aved options spécifiées (switches)
    tet.tetrahedralize(order=1,switches='-a4.0')

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

def handleNodes(nb_nodes, out_path):
    ''' Creation du fichier txt definissant les proprietes fixed et handle des noeuds d'un maillage
   nb_nodes : nombre de noeuds du fichier
   out_path : chemin vers le fichier txt a ecrire
   '''
   # Pour l'instant, tous les noeuds ont comme propriétés isFixed = 0 / isHandle = 1
    with open(out_path, 'w') as file:
        for i in range(1, nb_nodes + 1):
            file.write(f"{i}:0:1:\n")
    print("Generation de ",out_path, "terminee")

def get_vertices_count(file_path):
    ''' Recupere le nombre de sommets d'un fichier tet (ecrit sur la 1ere ligne)
    file_path: Chemin du fichier texte
    return: Le nombre entier extrait de la premiere ligne.
    '''
    with open(file_path, 'r') as file:
        first_line = file.readline()
        number = int(first_line.split()[0])
        return number