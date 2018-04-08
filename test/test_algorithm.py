# =============================================================================
#
#  Copyright (c) 2017, Justin Chadwell.
#
#  This program is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You can find a copy of the GNU General Public License in the LICENSE file.
#  Alternatively, see <http://www.gnu.org/licenses/>.
#
# =============================================================================

import unittest

import mpw.algorithm

# tests adopted from
# https://github.com/Lyndir/MasterPassword/blob/master/core/mpw_tests.xml

def helper(version=-1, name='Robert Lee Mitchell',
        master_password='banana colored duckling',
        site='masterpasswordapp.com', counter=1, template='long'):
    gen = mpw.algorithm.Algorithm(version)
    key = gen.generate_key(master_password, name)
    site_password = gen.generate_password(key, site, counter, template)

    return site_password

class TestAlgorithmV0(unittest.TestCase):
    def test_core(self):
        password = helper(version=0)
        self.assertEqual(password, 'Feji5@ReduWosh')

    def test_name(self):
        password = helper(version=0, name='⛄')
        self.assertEqual(password, 'HajrYudo7@Mamh')

    def test_master_password(self):
        password = helper(version=0, master_password='⛄')
        self.assertEqual(password, 'MewmDini0]Meho')

    def test_site(self):
        password = helper(version=0, site='⛄')
        self.assertEqual(password, 'HahiVana2@Nole')

    def test_template_maximum(self):
        password = helper(version=0, template='maximum')
        self.assertEqual(password, 'w1!3bA3icmRAc)SS@lwl')

    def test_template_medium(self):
        password = helper(version=0, template='medium')
        self.assertEqual(password, 'Fej7]Jug')

    def test_template_basic(self):
        password = helper(version=0, template='basic')
        self.assertEqual(password, 'wvH7irC1')

    def test_template_short(self):
        password = helper(version=0, template='short')
        self.assertEqual(password, 'Fej7')

    def test_template_pin(self):
        password = helper(version=0, template='pin')
        self.assertEqual(password, '2117')

    def test_template_name(self):
        password = helper(version=0, template='name')
        self.assertEqual(password, 'fejrajugo')

    def test_template_phrase(self):
        password = helper(version=0, template='phrase')
        self.assertEqual(password, 'fejr jug gabsibu bax')

class TestAlgorithmV1(unittest.TestCase):
    def test_core(self):
        password = helper(version=1)
        self.assertEqual(password, 'Jejr5[RepuSosp')

    def test_name(self):
        password = helper(version=1, name='⛄')
        self.assertEqual(password, 'WaqoGuho2[Xaxw')

    def test_master_password(self):
        password = helper(version=1, master_password='⛄')
        self.assertEqual(password, 'QesuHirv5-Xepl')

    def test_site(self):
        password = helper(version=1, site='⛄')
        self.assertEqual(password, 'WawiYarp2@Kodh')

    def test_template_maximum(self):
        password = helper(version=1, template='maximum')
        self.assertEqual(password, 'W6@692^B1#&@gVdSdLZ@')

    def test_template_medium(self):
        password = helper(version=1, template='medium')
        self.assertEqual(password, 'Jej2$Quv')

    def test_template_basic(self):
        password = helper(version=1, template='basic')
        self.assertEqual(password, 'WAo2xIg6')

    def test_template_short(self):
        password = helper(version=1, template='short')
        self.assertEqual(password, 'Jej2')

    def test_template_pin(self):
        password = helper(version=1, template='pin')
        self.assertEqual(password, '7662')

    def test_template_name(self):
        password = helper(version=1, template='name')
        self.assertEqual(password, 'jejraquvo')

    def test_template_phrase(self):
        password = helper(version=1, template='phrase')
        self.assertEqual(password, 'jejr quv cabsibu tam')

class TestAlgorithmV2(unittest.TestCase):
    def test_core(self):
        password = helper(version=2)
        self.assertEqual(password, 'Jejr5[RepuSosp')

    def test_name(self):
        password = helper(version=2, name='⛄')
        self.assertEqual(password, 'WaqoGuho2[Xaxw')

    def test_master_password(self):
        password = helper(version=2, master_password='⛄')
        self.assertEqual(password, 'QesuHirv5-Xepl')

    def test_site(self):
        password = helper(version=2, site='⛄')
        self.assertEqual(password, 'LiheCuwhSerz6)')

    def test_template_maximum(self):
        password = helper(version=2, template='maximum')
        self.assertEqual(password, 'W6@692^B1#&@gVdSdLZ@')

    def test_template_medium(self):
        password = helper(version=2, template='medium')
        self.assertEqual(password, 'Jej2$Quv')

    def test_template_basic(self):
        password = helper(version=2, template='basic')
        self.assertEqual(password, 'WAo2xIg6')

    def test_template_short(self):
        password = helper(version=2, template='short')
        self.assertEqual(password, 'Jej2')

    def test_template_pin(self):
        password = helper(version=2, template='pin')
        self.assertEqual(password, '7662')

    def test_template_name(self):
        password = helper(version=2, template='name')
        self.assertEqual(password, 'jejraquvo')

    def test_template_phrase(self):
        password = helper(version=2, template='phrase')
        self.assertEqual(password, 'jejr quv cabsibu tam')

class TestAlgorithmV3(unittest.TestCase):
    def test_core(self):
        password = helper(version=3)
        self.assertEqual(password, 'Jejr5[RepuSosp')

    def test_name(self):
        password = helper(version=3, name='⛄')
        self.assertEqual(password, 'NopaDajh8=Fene')

    def test_master_password(self):
        password = helper(version=3, master_password='⛄')
        self.assertEqual(password, 'QesuHirv5-Xepl')

    def test_site(self):
        password = helper(version=3, site='⛄')
        self.assertEqual(password, 'LiheCuwhSerz6)')

    def test_template_maximum(self):
        password = helper(version=3, template='maximum')
        self.assertEqual(password, 'W6@692^B1#&@gVdSdLZ@')

    def test_template_medium(self):
        password = helper(version=3, template='medium')
        self.assertEqual(password, 'Jej2$Quv')

    def test_template_basic(self):
        password = helper(version=3, template='basic')
        self.assertEqual(password, 'WAo2xIg6')

    def test_template_short(self):
        password = helper(version=3, template='short')
        self.assertEqual(password, 'Jej2')

    def test_template_pin(self):
        password = helper(version=3, template='pin')
        self.assertEqual(password, '7662')

    def test_template_name(self):
        password = helper(version=3, template='name')
        self.assertEqual(password, 'jejraquvo')

    def test_template_phrase(self):
        password = helper(version=3, template='phrase')
        self.assertEqual(password, 'jejr quv cabsibu tam')
