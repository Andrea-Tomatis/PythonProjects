'''
Co-author Network


¬Andrea-Tomatis
'''

from scholarly import scholarly
import psycopg2
import matplotlib.pyplot as plt
import networkx as nx
import PIL
import urllib.request
import math
import matplotlib.image as mpimg



#the names of the authors to display
#AUT_NAME = ["Franco Perracchi", "Michele Boldrin"]#, "Ping Wang", "Jordan Peterson", "Francesco Malaspina", "Kun Zhu", "Andrea Rossi", "Rodrigo S. Verdi"]
AUT_NAME = ["Ping Wang", "Jordan Peterson", "Chris Westbury"]


def get_authors(name):
    # Retrieve the first result from the iterator
    search_query = scholarly.search_author(name)
    authors = []
    try:
        author_result = next(search_query)
        while author_result != None:
            authors.append(author_result)
            author_result = next(search_query)
    except StopIteration:
        pass
    
    return authors


def isInDb(author):
    conn = psycopg2.connect(database="ProjectErdos",
                        host="localhost",
                        user="postgres",
                        password="admin",
                        port="5432")

    cursor = conn.cursor()

    cursor.execute(f"""
                   SELECT * FROM authors
                   WHERE scholar_id = '{author["scholar_id"]}'                
                   """)
    
    result = cursor.fetchone()
    

    conn.commit()
    cursor.close()

    print(f"search result: {result}")

    if result == None:
        return -1
    elif not result[-1]:
        return 0
    else: 
        return 1



def add_author(a, hub=None):
    try:

        conn = psycopg2.connect(database="ProjectErdos",
                            host="localhost",
                            user="postgres",
                            password="admin",
                            port="5432")
        cursor = conn.cursor()
        
        if hub is None:
            cursor.execute(f"""
                    INSERT INTO authors (scholar_id, name, affiliation, email, citedby, url_picture, is_hub)
                    VALUES ('{a["scholar_id"]}','{a["name"]}','{a["affiliation"]}','{a["email_domain"]}','{a["citedby"]}','{a["url_picture"]}','True')    
                    """)
        else:
            cursor.execute(f"""
                        INSERT INTO authors (scholar_id, name, affiliation, is_hub)
                        VALUES ('{a["scholar_id"]}','{a["name"]}','{a["affiliation"]}','False')    
                        """)
        
            cursor.execute(f"""
                        INSERT INTO Pubblications (hub_id, secondary_id)
                        VALUES ('{hub["scholar_id"]}','{a["scholar_id"]}')    
                        """)
        
        conn.commit()
        cursor.close()
        
    except Exception as e:
        print(e)
        return False
    
    return True


def update_hub(author):

    try:
        conn = psycopg2.connect(database="ProjectErdos",
                            host="localhost",
                            user="postgres",
                            password="admin",
                            port="5432")

        cursor = conn.cursor()

        cursor.execute(f"""
                    UPDATE authors
                    SET is_hub = 'True', url_picture = '{author['url_picture']}', email = '{author['email_domain']}', citedby = '{author['citedby']}'
                    WHERE scholar_id = '{author["scholar_id"]}'                
                    """)
    except Exception as e:
        print(f"Update failed. {e}")
    finally:
        conn.commit()
        cursor.close()


def get_nodes_from_db(author):
    try:
        conn = psycopg2.connect(database="ProjectErdos",
                                host="localhost",
                                user="postgres",
                                password="admin",
                                port="5432")
        cursor = conn.cursor()

        cursor.execute(f"""
                       SELECT secondary_id 
                       FROM pubblications
                       WHERE hub_id = '{author["scholar_id"]}' 
                    """)
        secondary = cursor.fetchall()
        nodes = []
        
        for el in secondary:
            cursor.execute(f"""
                       SELECT * 
                       FROM authors
                       WHERE scholar_id = '{el[0]}'
                    """)
            nodes.append(cursor.fetchall()[0])
        
        
        cursor.execute(f"""
                       SELECT hub_id 
                       FROM pubblications
                       WHERE secondary_id = '{author["scholar_id"]}'
                    """)
        secondary = cursor.fetchall()
        for el in secondary:
            cursor.execute(f"""
                       SELECT * 
                       FROM authors
                       WHERE scholar_id = '{el[0]}'
                    """)
            nodes.append(cursor.fetchall()[0])


        conn.close()
        cursor.close()
        
        #remodelling the data structure to match the graph requirements
        out = []
        for n in nodes:
            out.append({"scholar_id":n[0],
                        "name" : n[1],
                        "affiliation": n[2],
                        "email_domain": n[3],
                        "citedby" : n[4],
                        "picture" : n[5]})
        return out
    except Exception as e:
        print(f"Anable to read the data. {e}")
        return []


def get_nodes_from_net(author):
    # Retrieve all the details for the author
    if "'" in author["name"]:
        author["name"] = author["name"].replace("'","''")
    if "'" in author["affiliation"]:
        author["affiliation"] = author["affiliation"].replace("'","''")

    try:

        if not add_author(author, hub=None):
            print(f"The insertion of {author['scholar_id']} failed")

        co_authors = scholarly.fill(author)
        for c in co_authors["coauthors"]:
            if "'" in c["name"]:
                c["name"] = c["name"].replace("'","''")
            if "'" in c["affiliation"]:
                c["affiliation"] = c["affiliation"].replace("'","''")
        
        for a in co_authors["coauthors"]:
            if not add_author(a, hub=author):
                print(f"The insertion of {a['scholar_id']} failed")
            
       

    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
    return co_authors["coauthors"]



def draw_graph(G, labels, hubs_id):
    # Get a reproducible layout and create figure

    fig, ax = plt.subplots(figsize=(18, 7))
    pos = nx.spring_layout(G,k=0.2)


    # Note: the min_source/target_margin kwargs only work with FancyArrowPatch objects.
    # Force the use of FancyArrowPatch for edge drawing by setting `arrows=True`,
    # but suppress arrowheads with `arrowstyle="-"`
    nx.draw_networkx_edges(
        G,
        pos=pos,
        ax=ax,
        arrows=True,
        arrowstyle="-",
        min_source_margin=15,
        min_target_margin=15,
    )

    nx.draw(G, pos, with_labels=False, node_color='green', edge_color='green', node_size=40)

    fig.set_facecolor("#00000F")
    ax.set_facecolor("#00000F")

    for key, l in labels.items():
        labels[key] = '\n'.join(l.split(' '))
    #label_pos = {k: (v[0], v[1] + 0.12) for k, v in pos.items()}
    label_options = {"ec": "k", "fc": "white",'boxstyle':'round,pad=0.1', "alpha": 0.7}
    nx.draw_networkx_labels(G, pos, labels, font_family='monospacext', font_size=9, font_color='green', verticalalignment='center',font_weight='bold', bbox=label_options)

    # Transform from data coordinates (scaled between xlim and ylim) to display coordinates
    tr_figure = ax.transData.transform
    # Transform from display to figure coordinates
    tr_axes = fig.transFigure.inverted().transform

    # Select the size of the image (relative to the X axis)
    icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0])  * 0.025
    hub_size = (ax.get_xlim()[1] - ax.get_xlim()[0])  * 0.05
    icon_center = icon_size / 2.0

    
    # Add the respective image to each node
    for n in G.nodes:
        xf, yf = tr_figure(pos[n])
        xa, ya = tr_axes((xf, yf))
        # get overlapped axes and plot icon
        for k in hubs_id:
            if n == k["scholar_id"]:
                a = plt.axes([xa - icon_center, ya - icon_center, hub_size, hub_size])
                a.imshow(G.nodes[n]["image"])
                a.axis("off")
    
    plt.axis('off')
    plt.show()


def get_graph(hubs, G_nodes):

    images = []
    for i, hub in enumerate(hubs):
        urllib.request.urlretrieve(hub["url_picture"],f"hub_{i}.png")

        # Load images
        images.append(PIL.Image.open(f"hub_{i}.png"))

    # Generate the computer network graph
    G = nx.Graph()

    labels = {}

    #add hubs
    for i, hub in enumerate(hubs):
        G.add_node(hub["scholar_id"], image=images[i])
    
    for hub, nodes in G_nodes.items():
        for co_author in nodes:

            for h, n in G_nodes.items():
                if co_author in n:
                    # Load images
                    image = PIL.Image.open("icon.png")
                    if co_author['scholar_id'] not in [s['scholar_id'] for s in hubs]:
                        G.add_node(co_author["scholar_id"], image=image)
                    G.add_edge(h, co_author["scholar_id"])
                    labels[co_author['scholar_id']] = co_author['name']

    return G, labels


def main():
    authors = []
    G_nodes = {}
    ans = 0
    
    for i,n in enumerate(AUT_NAME):
        result = get_authors(n)
        authors.append(result[ans])

        in_stock = isInDb(result[ans])
        if in_stock == 1:
            nodes = get_nodes_from_db(result[ans])
        elif in_stock == 0:
            update_hub(result[0])
            nodes = get_nodes_from_net(result[ans])
        elif in_stock == -1:
            nodes = get_nodes_from_net(result[ans])
        G_nodes[result[ans]["scholar_id"]] = nodes
    
    G, labels = get_graph(authors, G_nodes)
    draw_graph(G, labels, authors)
    

if __name__ == "__main__":
    main()