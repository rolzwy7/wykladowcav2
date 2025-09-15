"""RBL Check Init"""

# flake8: noqa=E501
# pylint: disable=missing-class-docstring

from django.core.management.base import BaseCommand

from core.models import ListRBL


class Command(BaseCommand):
    help = "Wypełnia model ListRBL predefiniowaną listą serwerów RBL."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("Rozpoczynam wypełnianie bazy danych listami RBL...")
        )

        rbl_servers = [
            "zombie.dnsbl.sorbs.net",
            "ix.dnsbl.manitu.net",
            "bl.spamcop.net",
            "dsn.rfc-ignorant.org",
            "multi.surbl.org",
            "cblless.anti-spam.org.cn",
            "cblplus.anti-spam.org.cn",
            "cbl.anti-spam.org.cn",
            "blackholes.five-ten-sg.com",
            "sorbs.dnsbl.net.au",
            "dnsbl.sorbs.net",
            "db.wpbl.info",
            "rmst.dnsbl.net.au",
            "dnsbl.kempt.net",
            "blacklist.woody.ch",
            "psbl.surriel.com",
            "virbl.bit.nl",
            "rot.blackhole.cantv.net",
            "virus.rbl.jp",
            "wormrbl.imp.ch",
            "spamrbl.imp.ch",
            "rbl.interserver.net",
            "spamlist.or.kr",
            "dyna.spamrats.com",
            "dnsbl.abuse.ch",
            "dnsbl.inps.de",
            "dnsbl.dronebl.org",
            "bl.deadbeef.com",
            "ricn.dnsbl.net.au",
            "forbidden.icm.edu.pl",
            "probes.dnsbl.net.au",
            "ubl.unsubscore.com",
            "b.barracudacentral.org",
            "ksi.dnsbl.net.au",
            "uribl.swinog.ch",
            "bsb.spamlookup.net",
            "dob.sibl.support-intelligence.net",
            "url.rbl.jp",
            "dyndns.rbl.jp",
            "bogons.cymru.com",
            "relays.mail-abuse.org",
            "omrs.dnsbl.net.au",
            "osrs.dnsbl.net.au",
            "orvedb.aupads.org",
            "relays.nether.net",
            "relays.bl.gweep.ca",
            "smtp.dnsbl.sorbs.net",
            "relays.bl.kundenserver.de",
            "dialups.mail-abuse.org",
            "rdts.dnsbl.net.au",
            "spam.dnsbl.sorbs.net",
            "duinv.aupads.org",
            "dynablock.sorbs.net",
            "dynip.rothen.com",
            "dul.blackhole.cantv.net",
            "cdl.anti-spam.org.cn",
            "short.rbl.jp",
            "korea.services.net",
            "mail.people.it",
            "blacklist.sci.kun.nl",
            "all.spamblock.unit.liu.se",
            "dnsbl.tornevall.org",
            "rhsbl.rbl.polspam.pl",
            "bl-h2.rbl.polspam.pl",
            "bl.octopusdns.com",
            "superblock.ascams.com",
            "dnsbl.justspam.org",
            "zen.spamhaus.org",
            "cbl.abuseat.org",
            "dnsbl-1.uceprotect.net",
            "dnsbl-2.uceprotect.net",
            "bl.mailspike.net",
            "z.mailspike.net",
            "rbl.spamlab.com",
            "truncate.gbudb.net",
        ]

        created_count = 0
        skipped_count = 0

        for server_address in rbl_servers:
            _, created = ListRBL.manager.get_or_create(address=server_address.lower())

            if created:
                self.stdout.write(f"  [+] Dodano: {server_address}")
                created_count += 1
            else:
                skipped_count += 1

        if skipped_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    f"\nPominięto {skipped_count} list, które już istniały w bazie."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(f"\nDodano {created_count} nowych list RBL.")
        )
        self.stdout.write(self.style.SUCCESS("Zakończono zadanie."))
