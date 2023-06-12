from django.core.management.base import BaseCommand
from lojinha.models import Customer

class Command(BaseCommand):
    """
    Comando para criar os customers, pois ninguém merece digitar essa parada.
    """
    help = 'Cria os customers.'

    def handle(self, *args, **kwargs):
        customers = [
            {'name': 'Tom', 'phone': '4444444444', 'email': 'tom@tom.com', 'image': 'customers/tom.jpg'},
            {'name': 'Spike', 'phone': '2222222222', 'email': 'spike@spike.com', 'image': 'customers/spike.jpg'},
            {'name': 'Jerry', 'phone': '3333333333', 'email': 'jerry@jerry.com', 'image': 'customers/jerry.jpg'},
            {'name': 'Tyke', 'phone': '5555555555', 'email': 'tyke@tyke.com', 'image': 'customers/tyke.jpg'},
            {'name': 'Wile E. Coyote', 'phone': '6666666666', 'email': 'wile@coyote.com', 'image': 'customers/wile.jpg'},  # noqa: E501
            {'name': 'Road Runner', 'phone': '7777777777', 'email': 'road@runner.com', 'image': 'customers/road.jpg'},
            {'name': 'Mickey Mouse', 'phone': '1111111111', 'email': 'mickey@mouse.com', 'image': 'customers/mickey.jpg'},  # noqa: E501
            {'name': 'Donald Duck', 'phone': '2222222222', 'email': 'donald@duck.com', 'image': 'customers/donald.jpg'},
            {'name': 'SpongeBob SquarePants', 'phone': '3333333333', 'email': 'spongebob@spongepants.com', 'image': 'customers/spongebob.jpg'},  # noqa: E501
            {'name': 'Patrick Star', 'phone': '4444444444', 'email': 'patrick@star.com', 'image': 'customers/patrick.jpg'},  # noqa: E501
            {'name': 'Scooby-Doo', 'phone': '6666666666', 'email': 'scooby@doo.com', 'image': 'customers/scooby.jpg'},
            {'name': 'Fred Flintstone', 'phone': '7777777777', 'email': 'fred@flintstone.com', 'image': 'customers/fred.jpg'},  # noqa: E501
            {'name': 'Wilma Flintstone', 'phone': '8888888888', 'email': 'wilma@flintstone.com', 'image': 'customers/wilma.jpg'},  # noqa: E501
            {'name': 'Popeye', 'phone': '9999999999', 'email': 'popeye@sailor.com', 'image': 'customers/popeye.jpg'},
            {'name': 'Olive Oyl', 'phone': '1010101010', 'email': 'olive@oyl.com', 'image': 'customers/olive.jpg'},
            {'name': 'Homer Simpson', 'phone': '3333333333', 'email': 'homer@simpson.com', 'image': 'customers/homer.jpg'},  # noqa: E501
            {'name': 'Bart Simpson', 'phone': '4444444444', 'email': 'bart@simpson.com', 'image': 'customers/bart.jpg'},
            {'name': 'Lisa Simpson', 'phone': '5555555555', 'email': 'lisa@simpson.com', 'image': 'customers/lisa.jpg'},
            {'name': 'Marge Simpson', 'phone': '6666666666', 'email': 'marge@simpson.com', 'image': 'customers/marge.jpg'},  # noqa: E501
            {'name': 'Snoopy', 'phone': '7777777777', 'email': 'snoopy@peanuts.com', 'image': 'customers/snoopy.jpg'},
            {'name': 'Charlie Brown', 'phone': '8888888888', 'email': 'charlie@brown.com', 'image': 'customers/charlie.jpg'},  # noqa: E501
            {'name': 'Shaggy Rogers', 'phone': '2222222222', 'email': 'shaggy@rogers.com', 'image': 'customers/shaggy.jpg'},  # noqa: E501
            {'name': 'Minnie Mouse', 'phone': '8888888888', 'email': 'minnie@mouse.com', 'image': 'customers/minnie.jpg'},  # noqa: E501
            {'name': 'Daisy Duck', 'phone': '9999999999', 'email': 'daisy@duck.com', 'image': 'customers/daisy.jpg'},
            {'name': 'Winnie the Pooh', 'phone': '1010101010', 'email': 'winnie@pooh.com', 'image': 'customers/winnie.jpg'},  # noqa: E501
            {'name': 'Goofy', 'phone': '5555555555', 'email': 'goofy@goofy.com', 'image': 'customers/goofy.jpg'},
            {'name': 'Lola Bunny', 'phone': '3333333333', 'email': 'lola@bunny.com', 'image': 'customers/lola.jpg'},
            {'name': 'Porky Pig', 'phone': '4444444444', 'email': 'porky@pig.com', 'image': 'customers/porky.jpg'},
            {'name': 'Buster Bunny', 'phone': '1111111111', 'email': 'buster@bunny.com', 'image': 'customers/buster.jpg'},  # noqa: E501
            {'name': 'Babs Bunny', 'phone': '2222222222', 'email': 'babs@bunny.com', 'image': 'customers/babs.jpg'},
            {'name': 'Plucky Duck', 'phone': '3333333333', 'email': 'plucky@duck.com', 'image': 'customers/plucky.jpg'},
            {'name': 'Hamton J. Pig', 'phone': '4444444444', 'email': 'hamton@pig.com', 'image': 'customers/hamton.jpg'},  # noqa: E501
            {'name': 'Elmyra Duff', 'phone': '5555555555', 'email': 'elmyra@duff.com', 'image': 'customers/elmyra.jpg'},
            {'name': 'Furrball', 'phone': '6666666666', 'email': 'furrball@cat.com', 'image': 'customers/furrball.jpg'},
            {'name': 'Hamton J. Pig', 'phone': '4444444444', 'email': 'hamton@pig.com', 'image': 'customers/hamton.jpg'}, # noqa: E501
            {'name': 'Elmyra Duff', 'phone': '5555555555', 'email': 'elmyra@duff.com', 'image': 'customers/elmyra.jpg'},
            {'name': 'Fred Jones', 'phone': '3333333333', 'email': 'fred@jones.com', 'image': 'customers/fred.jpg'},
            {'name': 'Daphne Blake', 'phone': '4444444444', 'email': 'daphne@blake.com', 'image': 'customers/daphne.jpg'}, # noqa: E501
            {'name': 'Velma Dinkley', 'phone': '5555555555', 'email': 'velma@dinkley.com', 'image': 'customers/velma.jpg'}, # noqa: E501
            {'name': 'Hank', 'phone': '1111111111', 'email': 'hank@caverna.com', 'image': 'customers/hank.jpg'},
            {'name': 'Eric', 'phone': '2222222222', 'email': 'eric@caverna.com', 'image': 'customers/eric.jpg'},
            {'name': 'Diana', 'phone': '3333333333', 'email': 'diana@caverna.com', 'image': 'customers/diana.jpg'},
            {'name': 'Presto', 'phone': '4444444444', 'email': 'presto@caverna.com', 'image': 'customers/presto.jpg'},
            {'name': 'Sheila', 'phone': '5555555555', 'email': 'sheila@caverna.com', 'image': 'customers/sheila.jpg'},
            {'name': 'Bobby', 'phone': '6666666666', 'email': 'bobby@caverna.com', 'image': 'customers/bobby.jpg'},
            {'name': 'Mestre dos Magos', 'phone': '8888888888', 'email': 'mestre@caverna.com', 'image': 'customers/mestre.jpg'}, # noqa: E501
            {'name': 'Vingador', 'phone': '9999999999', 'email': 'vingador@caverna.com', 'image': 'customers/vingador.jpg'}, # noqa: E501
            {'name': 'Winnie', 'phone': '2222222222', 'email': 'winnie@pica-pau.com', 'image': 'customers/winnie.jpg'},
            {'name': 'Buzz Buzzard', 'phone': '3333333333', 'email': 'buzz@buzzard.com', 'image': 'customers/buzz.jpg'},
            {'name': 'Splinter', 'phone': '4444444444', 'email': 'splinter@pica-pau.com', 'image': 'customers/splinter.jpg'}, # noqa: E501
            {'name': 'Andy Panda', 'phone': '5555555555', 'email': 'andy@panda.com', 'image': 'customers/andy.jpg'},
            {'name': 'Chilly Willy', 'phone': '6666666666', 'email': 'chilly@willy.com', 'image': 'customers/chilly.jpg'}, # noqa: E501
            {'name': 'Knothead', 'phone': '7777777777', 'email': 'knothead@pica-pau.com', 'image': 'customers/knothead.jpg'}, # noqa: E501
            {'name': 'Splinter', 'phone': '8888888888', 'email': 'splinter@pica-pau.com', 'image': 'customers/splinter.jpg'}, # noqa: E501
            {'name': 'Felix The Cat', 'phone': '8888888888', 'email': 'felix@thecat.com', 'image': 'customers/felix.jpg'}, # noqa: E501
            {'name': 'Yogi Bear', 'phone': '1111111111', 'email': 'yogi@bear.com', 'image': 'customers/yogi.jpg'},
            {'name': 'Boo-Boo Bear', 'phone': '2222222222', 'email': 'booboo@bear.com', 'image': 'customers/booboo.jpg'}, # noqa: E501
            {'name': 'Ranger Smith', 'phone': '3333333333', 'email': 'ranger@smith.com', 'image': 'customers/ranger.jpg'},  # noqa: E501
            {'name': 'Cindy Bear', 'phone': '4444444444', 'email': 'cindy@bear.com', 'image': 'customers/cindy.jpg'},
            {'name': 'Mayor Brown', 'phone': '5555555555', 'email': 'mayor@brown.com', 'image': 'customers/mayor.jpg'},
            {'name': 'Ranger Jones', 'phone': '6666666666', 'email': 'ranger@jones.com', 'image': 'customers/ranger_jones.jpg'},  # noqa: E501
            {'name': 'Snagglepuss', 'phone': '7777777777', 'email': 'snagglepuss@cartoon.com', 'image': 'customers/snagglepuss.jpg'},  # noqa: E501
            {'name': 'Magilla Gorilla', 'phone': '8888888888', 'email': 'magilla@gorilla.com', 'image': 'customers/magilla.jpg'}, # noqa: E501
            {'name': 'Dick Dastardly', 'phone': '1111111111', 'email': 'dick@dastardly.com', 'image': 'customers/dick_dastardly.jpg'}, # noqa: E501
            {'name': 'Muttley', 'phone': '2222222222', 'email': 'muttley@dog.com', 'image': 'customers/muttley.jpg'},
            {'name': 'Penelope Pitstop', 'phone': '3333333333', 'email': 'penelope@pitstop.com', 'image': 'customers/penelope_pitstop.jpg'}, # noqa: E501
            {'name': 'Peter Perfect', 'phone': '4444444444', 'email': 'peter@perfect.com', 'image': 'customers/peter_perfect.jpg'}, # noqa: E501
            {'name': 'The Gruesome Twosome', 'phone': '5555555555', 'email': 'gruesome@twosome.com', 'image': 'customers/gruesome_twosome.jpg'}, # noqa: E501
            {'name': 'Professor Pat Pending', 'phone': '6666666666', 'email': 'professor@pending.com', 'image': 'customers/professor_pat_pending.jpg'}, # noqa: E501
            {'name': 'Red Max', 'phone': '7777777777', 'email': 'red@max.com', 'image': 'customers/red_max.jpg'},
            {'name': 'Sergeant Blast', 'phone': '8888888888', 'email': 'sergeant@blast.com', 'image': 'customers/sergeant_blast.jpg'}, # noqa: E501
            {'name': 'Top Cat', 'phone': '1111111111', 'email': 'topcat@cat.com', 'image': 'customers/topcat.jpg'},
            {'name': 'Benny the Ball', 'phone': '2222222222', 'email': 'benny@ball.com', 'image': 'customers/benny.jpg'}, # noqa: E501
            {'name': 'Fancy-Fancy', 'phone': '3333333333', 'email': 'fancy@fancy.com', 'image': 'customers/fancy.jpg'},
            {'name': 'Spook', 'phone': '4444444444', 'email': 'spook@cat.com', 'image': 'customers/spook.jpg'},
            {'name': 'Brain', 'phone': '5555555555', 'email': 'brain@cat.com', 'image': 'customers/brain.jpg'},
            {'name': 'Officer Dibble', 'phone': '6666666666', 'email': 'officer@dibble.com', 'image': 'customers/officer_dibble.jpg'}, # noqa: E501
            {'name': 'Choo-Choo', 'phone': '7777777777', 'email': 'choochoo@cat.com', 'image': 'customers/choochoo.jpg'}, # noqa: E501
            {'name': 'The Maharajah of Pookajee', 'phone': '8888888888', 'email': 'maharajah@pookajee.com', 'image': 'customers/maharajah.jpg'}, # noqa: E501
            {'name': 'Moe Szyslak', 'phone': '1111111111', 'email': 'moe@szyslak.com', 'image': 'customers/moe.jpg'},
            {'name': 'Ned Flanders', 'phone': '2222222222', 'email': 'ned@flanders.com', 'image': 'customers/ned.jpg'},
            {'name': 'Apu Nahasapeemapetilon', 'phone': '3333333333', 'email': 'apu@nahasapeemapetilon.com', 'image': 'customers/apu.jpg'}, # noqa: E501
            {'name': 'Chief Wiggum', 'phone': '4444444444', 'email': 'chief@wiggum.com', 'image': 'customers/wiggum.jpg'}, # noqa: E501
            {'name': 'Maggie Roswell', 'phone': '5555555555', 'email': 'maggie@roswell.com', 'image': 'customers/maggie.jpg'}, # noqa: E501
            {'name': 'Groundskeeper Willie', 'phone': '6666666666', 'email': 'groundskeeper@willie.com', 'image': 'customers/willie.jpg'}, # noqa: E501
            {'name': 'Sideshow Bob', 'phone': '7777777777', 'email': 'sideshow@bob.com', 'image': 'customers/bob.jpg'},
            {'name': 'Dr. Julius Hibbert', 'phone': '8888888888', 'email': 'dr@hibbert.com', 'image': 'customers/hibbert.jpg'}, # noqa: E501
            {'name': 'Carmen Sandiego', 'phone': '1111111111', 'email': 'carmen@sandiego.com', 'image': 'customers/carmen_sandiego.jpg'}, # noqa: E501
            {'name': 'Ivy', 'phone': '4444444444', 'email': 'ivy@carmensandiego.com', 'image': 'customers/ivy.jpg'},
            {'name': 'Zack', 'phone': '5555555555', 'email': 'zack@carmensandiego.com', 'image': 'customers/zack.jpg'},
            {'name': 'Timon', 'phone': '1111111111', 'email': 'timon@lionking.com', 'image': 'customers/timon.jpg'},
            {'name': 'Pumbaa', 'phone': '2222222222', 'email': 'pumbaa@lionking.com', 'image': 'customers/pumbaa.jpg'},
            {'name': 'Yakko', 'phone': '3333333333', 'email': 'yakko@animaniacs.com', 'image': 'customers/yakko.jpg'}, # noqa: E501
            {'name': 'Wakko', 'phone': '4444444444', 'email': 'wakko@animaniacs.com', 'image': 'customers/wakko.jpg'}, # noqa: E501
            {'name': 'Dot', 'phone': '5555555555', 'email': 'dot@animaniacs.com', 'image': 'customers/dot.jpg'},
            {'name': 'Pink Panther', 'phone': '6666666666', 'email': 'pink@panther.com', 'image': 'customers/pink_panther.jpg'}, # noqa: E501
            {'name': 'Pepe Le Pew', 'phone': '1111111111', 'email': 'pepe@lepew.com', 'image': 'customers/pepe_le_pew.jpg'}, # noqa: E501
            {'name': 'Squidward Tentacles', 'phone': '2222222222', 'email': 'squidward@tentacles.com', 'image': 'customers/squidward_tentacles.jpg'}, # noqa: E501
            {'name': 'Quick Draw McGraw', 'phone': '3333333333', 'email': 'quick@draw.com', 'image': 'customers/quick_draw_mcgraw.jpg'}, # noqa: E501
            {'name': 'Speed Racer', 'phone': '4444444444', 'email': 'speed@racer.com', 'image': 'customers/speed_racer.jpg'}, # noqa: E501
            {'name': 'Swee Pea', 'phone': '5555555555', 'email': 'sweepea@popeye.com', 'image': 'customers/sweepea.jpg'}, # noqa: E501
            {'name': 'Brutus', 'phone': '6666666666', 'email': 'brutus@popeye.com', 'image': 'customers/brutus.jpg'},
            {'name': 'Chip and Dale', 'phone': '7777777777', 'email': 'chipanddale@disney.com', 'image': 'customers/chip_and_dale.jpg'}, # noqa: E501
            {'name': 'Pinky and the Brain', 'phone': '8888888888', 'email': 'pinkyandbrain@animaniacs.com', 'image': 'customers/pinky_and_brain.jpg'}, # noqa: E501
            {'name': 'Doug Funnie', 'phone': '9999999999', 'email': 'doug@funnie.com', 'image': 'customers/doug_funnie.jpg'}, # noqa: E501
            {'name': 'Scrooge McDuck', 'phone': '1010101010', 'email': 'scrooge@ducktales.com', 'image': 'customers/scrooge_mcduck.jpg'}, # noqa: E501
            {'name': 'Launchpad McQuack', 'phone': '1212121212', 'email': 'launchpad@ducktales.com', 'image': 'customers/launchpad_mcquack.jpg'}, # noqa: E501
            {'name': 'Taz', 'phone': '1313131313', 'email': 'taz@looneytunes.com', 'image': 'customers/taz.jpg'},
]


        for customer in customers:
            try:
                Customer.objects.create(name=customer['name'], phone=customer['phone'], email=customer['email'], image=customer['image'])  # noqa: E501
                self.stdout.write(self.style.SUCCESS(f'Customer {customer["name"]} importado com sucesso'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro ao importar o customer {customer["name"]}: {e}'))
