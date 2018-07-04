## some misc functions for embeddings

try: ## try to import the parallel variation
    from MulticoreTSNE import MulticoreTSNE as TSNE
    import multiprocessing as mp
    parallel_tsne = True
except ImportError:
    try:
        from sklearn.manifold import TSNE
        parallel_tsne = False
    except:
        pass

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_2d_coordinates_tsne(multinet,output_format="json",verbose=True):

    embedding = multinet.embedding
    X = embedding[0]
    indices = embedding[1]
    if verbose:
        multinet.monitor("Doing the TSNE reduction to 2 dimensions!")
    if parallel_tsne:
        X_embedded = TSNE(n_components=2,n_jobs=mp.cpu_count()).fit_transform(X)
    else:
        X_embedded = TSNE(n_components=2).fit_transform(X)

    dfr = pd.DataFrame(X_embedded,columns=['dim1','dim2'])
    dfr['node_names'] = [n for n in multinet.get_nodes()]
    dfr['node_codes'] = indices
    if output_format == "json":        
        ## export this as json
        return dfr.to_json(orient='records')
    
    elif output_format == "dataframe":
        ## pure pandas dataframe
        return dfr
    
    else:
        return None

