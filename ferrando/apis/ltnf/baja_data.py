import requests
import json
from typing import TypeAlias

RSession: TypeAlias = requests.Session

def asset_providers(session: RSession) -> json:
    """
    Retrieves all the asset providers
    """
    url = "https://fintual.cl/api/asset_providers"
    r= session.get(url)
    return r.json()
    
def asset_providers_data(asset_provider_id: int, session: RSession) -> json:
    """
    Retrieves specific asset provider data
    """
    url = f"https://fintual.cl/api/asset_providers/{asset_provider_id}"
    r= session.get(url)
    return r.json()

def banks(session:RSession) -> json:
    """
    Retrieves filtered banks
    """
    url = f"https://fintual.cl/api/banks"
    r= session.get(url)
    return r.json()

def conceptual_asset_by_provider(asset_provider_id: int, session: RSession) -> json:
    """
    Retrieves conceptual assets for the given provider
    """
    url = f"https://fintual.cl/api/asset_providers/{asset_provider_id}/conceptual_assets"
    r= session.get(url)
    return r.json()

def conceptual_assets(session: RSession) -> json:
    """
    Retrieves conceptual assets
    """
    url = f"https://fintual.cl/api/conceptual_assets"
    r= session.get(url)
    return r.json()

def conceptual_assets_data(conceptual_asset_id: int, session: RSession) -> json:
    """
    Retrieves conceptual assets
    """
    url = f"https://fintual.cl/api/conceptual_assets/{conceptual_asset_id}"
    r= session.get(url)
    return r.json() 

def real_assets_by_conceptual(conceptual_asset_id: int, session: RSession) -> json:
    """
    Retrieves all the real assets
    """
    url = f"https://fintual.cl/api/conceptual_assets/{conceptual_asset_id}/real_assets"
    r= session.get(url)
    return r.json() 

def real_assets_data(real_asset_id: int, session: RSession) -> json:
    """
    Retrieves specific real asset data
    """
    url = f"https://fintual.cl/api/real_assets/{real_asset_id}"
    r= session.get(url)
    return r.json() 

def real_assets_days(real_asset_id: int, session: RSession) -> json:
    """
    Retrieves specific real asset days
    """
    url = f"https://fintual.cl/api/real_assets/{real_asset_id}/days"
    r= session.get(url)
    return r.json() 

def real_asset_specific_date(real_asset_id: int, date:str, session: RSession) -> json:
    """
    Retrieves specific real asset days
    date es %Y-%m-%d
    """
    url = f"https://fintual.cl/api/real_assets/{real_asset_id}/days?date={date}"
    r= session.get(url)
    return r.json()

def real_asset_from_date(real_asset_id: int, from_date:str, session: RSession) -> json:
    """
    Retrieves specific real asset days
    date es %Y-%m-%d
    """
    url = f"https://fintual.cl/api/real_assets/{real_asset_id}/days?from_date={from_date}"
    r= session.get(url)
    return r.json()

def real_asset_to_date(real_asset_id: int, from_date:str, session: RSession) -> json:
    """
    Retrieves specific real asset days
    date es %Y-%m-%d
    """
    url = f"https://fintual.cl/api/real_assets/{real_asset_id}/days?to_date={from_date}"
    r= session.get(url)
    return r.json()

if __name__ == "__main__":
    with requests.Session() as session:
        proveedores = asset_providers(session=session)
        for proveedor in proveedores["data"]:
            nombre = proveedor["attributes"]["name"].upper()
            if "FOCUS" in nombre:
                print (proveedor)
    # {'id': '53', 'type': 'asset_provider', 'attributes': {'name': 'SOYFOCUS ADMINISTRADORA GENERAL DE FONDOS S.A.'}}    

        
        soyfocus_id = 53
        focus_ca = conceptual_asset_by_provider(asset_provider_id = 53, session = session)
        proveedores = focus_ca
        print (focus_ca)
    #{'data': [{'id': '2736', 'type': 'conceptual_asset', 'attributes': {'name': 'FONDO MUTUO CONSERVADOR FOCUS', 'symbol': 'FFMM-SOYFOCUS-9810', 'category': 'mutual_fund', 'currency': None, 'max_scale': 4, 'run': '9810-8', 'data_source': 'http://www.cmfchile.cl'}}, {'id': '2737', 'type': 'conceptual_asset', 'attributes': {'name': 'FONDO MUTUO ARRIESGADO FOCUS', 'symbol': 'FFMM-SOYFOCUS-9811', 'category': 'mutual_fund', 'currency': 'CLP', 'max_scale': 4, 'run': '9811-6', 'data_source': 'http://www.cmfchile.cl'}}, {'id': '2738', 'type': 'conceptual_asset', 'attributes': {'name': 'FONDO MUTUO MODERADO FOCUS', 'symbol': 'FFMM-SOYFOCUS-9809', 'category': 'mutual_fund', 'currency': 'CLP', 'max_scale': 4, 'run': '9809-4', 'data_source': 'http://www.cmfchile.cl'}}]}
        focus_conservador = 2736
        focus_moderado = 2738
        focus_arriesgado = 2737

        proveedores = real_assets_by_conceptual(conceptual_asset_id=2736, session=session)
        proveedores = conceptual_assets(session=session)

        print (proveedores["data"])
        claves = []
        categorias = []
        for proveedor in proveedores["data"]:
            print()
            print (proveedor)
            print (proveedor["attributes"].keys())
            claves.extend(list(proveedor["attributes"].keys()))
            print (proveedor["attributes"]["category"])
            categorias.append(proveedor["attributes"]["category"])
        print (set(claves))
        print (set(categorias))

        import json
        with open('data.json', 'w') as f:
            json.dump(proveedores, f, indent=4)

        # print (real_assets_by_conceptual(conceptual_asset_id=2500, session=session))
        # print ("="*30)
        # print (real_assets_data(real_asset_id=14900, session=session))
        # print ("="*30)
        # print (real_assets_days(real_asset_id=14900, session=session))
        # print ("="*30)
        # print (real_asset_specific_date(real_asset_id=14900, date="2015-10-02", session=session))
        # print ("="*30)
        # print (real_asset_from_date(real_asset_id=14901, from_date="2015-09-29", session=session))
        # print ("="*30)
        # print (real_asset_to_date(real_asset_id=14901, from_date="2015-09-29", session=session))