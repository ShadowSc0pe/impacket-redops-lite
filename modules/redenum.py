from impacket.smbconnection import SMBConnection
from impacket.dcerpc.v5 import transport, samr
from core.utils import print_banner, save_output
def run(target, username, password, domain=''):
    """
    Enumère les utilisateurs d'un domaine ou d'une machine locale via l'interface SAM-RPC.
    """
    print_banner("Module : Enumération des Utilisateurs")
    output = []
    try:
        # Connexion SMB authentifiée à la cible
        smb = SMBConnection(target, target)
        smb.login(username, password, domain)

        # Connexion RPC sur le service SAMR
        rpctransport = transport.SMBTransport(target, 445, r'\samr', smb_connection=smb)
        dce = rpctransport.get_dce_rpc()
        dce.connect()
        dce.bind(samr.MSRPC_UUID_SAMR)

        # Accès à la racine du gestionnaire de sécurité
        server_handle = samr.hSamrConnect(dce)['ServerHandle']
        # Récupération des domaines disponibles
        domains = samr.hSamrEnumerateDomainsInSamServer(dce, server_handle)['Buffer']['Buffer']
        domain_name = domains[0]['Name']
        # Résolution du SID du domaine
        domain_sid = samr.hSamrLookupDomainInSamServer(dce, server_handle, domain_name)['DomainId']
        # Ouverture du domaine pour énumération
        domain_handle = samr.hSamrOpenDomain(dce, server_handle, domain_sid)['DomainHandle']
        # Enumération des utilisateurs
        users = samr.hSamrEnumerateUsersInDomain(dce, domain_handle)['Buffer']['Buffer']
        for user in users:
            username = user['Name']
            output.append(username)
            print(f"[+] Utilisateur détecté : {username}")

        # Sauvegarde du résultat
        output_path = save_output(output, "users")
        print(f"[OK] Résultats enregistrés dans : {output_path}")
    except Exception as e:
        print(f"[ERREUR] Enumération échouée : {e}")