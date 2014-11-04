#! /usr/bin/env python

##############################################################################
##  pyvolve: Python platform for simulating evolutionary sequences.
##
##  Written by Stephanie J. Spielman (stephanie.spielman@gmail.com) 
##############################################################################

''' Test evolver under a variety of model specifications. Not quite unittests, but definitely tests.
    NOTE: as written, assumes no indels.
    
    TODO: Specific tests for CodonModel()
'''

import unittest
try:
    from pyvolve import *
except:
    try:
        import sys
        sys.path.append("../src/")
        from misc import *
        from newick import *
        from state_freqs import *
        from matrix_builder import *
        from evolver import *
    except:
        raise AssertionError("\nWhere's pyvolve!!")


class evolver_singlepart_nohet_tests(unittest.TestCase):
    ''' 
        Suite of tests for evolver under temporally homogeneous conditions (no branch heterogeneity!!)
        Single partition.
        All tests are conducted using nucleotides.
    '''
    
    def setUp(self):
        ''' 
            Tree and frequency set-up.
        '''
        self.tree = read_tree( tree = "(((t2:0.36,t1:0.45):0.001,t3:0.77):0.44,(t5:0.77,t4:0.41):0.89);" )
        f = EqualFrequencies(by = 'nuc')()
        
        m1 = Model()
        m1.params = {'state_freqs':f, 'mu':{'AC':1, 'AG':1, 'AT':1, 'CG':1, 'CT':1, 'GT':1}}
        m1.matrix = nucleotide_Matrix(m1)()
        self.part1 = Partition()
        self.part1.models = m1
        self.part1.size = 10

    
    def test_evolver_singlepart_nohet_ratefile(self):
        '''
            Test evolver with a single partition, no heterogeneity at all.
            Ensure rate file correct.
        '''
        
        evolve = Evolver(partitions = self.part1, tree = self.tree, ratefile = "rates.txt")()
        # Check ratefile
        with open('evolFiles/single_part_no_het_rates.txt', 'r') as ref_h:
            ref = str(ref_h.read())
        with open('rates.txt', 'r') as test_h:
            test = str(test_h.read())
        os.remove("rates.txt")
        self.assertMultiLineEqual(test, ref, msg = "Rate file improperly written for single partition, no het.")



    def test_evolver_singlepart_nohet_seqfile(self):
        '''
            Test evolver with a single partition, no heterogeneity at all.
            Ensure leaf sequences only properly written to seqfile.
        '''
        evolve = Evolver(partitions = self.part1, tree = self.tree, seqfile = "out.fasta")()
        
        # Check seqfile, no ancestors
        aln = AlignIO.read("out.fasta", "fasta")
        os.remove("out.fasta")
        assert(len(aln) == 5), "Wrong number of sequences were written to file when write_anc=False."
        assert(len(aln[0]) == 10), "Output alignment incorrect length."
        
        
    def test_evolver_singlepart_nohet_seqfile_anc(self):
        '''
            Test evolver with a single partition, no heterogeneity at all.
            Ensure ancestors properly written to seqfile.
        '''
        evolve = Evolver(partitions = self.part1, tree = self.tree, seqfile = "out.fasta", write_anc = True)()
        
        # Check seqfile, no ancestors
        aln = AlignIO.read("out.fasta", "fasta")
        os.remove("out.fasta")
        assert(len(aln) == 9), "Wrong number of sequences were written to file when write_anc=False."
        assert(len(aln[0]) == 10), "Output alignment incorrect length."
        

    def test_evolver_singlepart_nohet_seqfile_phy(self):
        '''
            Test evolver with a single partition, no heterogeneity at all.
            Ensure can save in phylip for seqfile.
        '''
        evolve = Evolver(partitions = self.part1, tree = self.tree, seqfile = "out.phy", seqfmt = "phylip")()
        
        # Check seqfile, no ancestors
        try:
            aln = AlignIO.read("out.phy", "phylip")
            os.remove("out.phy")
        except:
            raise AssertionError("Couldn't overwrite FASTA default to save as PHYLIP.")
            os.remove("out.phy")


class evolver_twopart_nohet_tests(unittest.TestCase):
    ''' 
        Suite of tests for evolver under temporally homogeneous conditions (no branch heterogeneity!!)
        Two partitions.
        All tests are conducted using nucleotides.
    '''
    
    def setUp(self):
        ''' 
            Tree and frequency set-up.
        '''
        self.tree = read_tree( tree = "(((t2:0.36,t1:0.45):0.001,t3:0.77):0.44,(t5:0.77,t4:0.41):0.89);" )
        f = EqualFrequencies(by = 'nuc')()
        
        m1 = Model()
        m1.params = {'state_freqs':f, 'mu':{'AC':1, 'AG':1, 'AT':1, 'CG':1, 'CT':1, 'GT':1}}
        m1.matrix = nucleotide_Matrix(m1)()
        self.part1 = Partition()
        self.part1.models = m1
        self.part1.size = 10
        
        m2 = Model()
        m2.params = {'state_freqs':f, 'mu':{'AC':1, 'AG':1, 'AT':1, 'CG':1, 'CT':1, 'GT':1}}
        m2.matrix = nucleotide_Matrix(m2)()
        self.part2 = Partition()
        self.part2.models = m2
        self.part2.size = 12
        
        
    def test_evolver_twopart_nohet_ratefile(self):
        '''
            Test evolver with two partitions, no heterogeneity at all.
            Ensure rate file correct.
        '''
        
        evolve = Evolver(partitions = [self.part1, self.part2], tree = self.tree, ratefile = "rates.txt")()
        # Check ratefile
        with open('evolFiles/two_part_no_het_rates.txt', 'r') as ref_h:
            ref = str(ref_h.read())
        with open('rates.txt', 'r') as test_h:
            test = str(test_h.read())
        os.remove("rates.txt")
        self.assertMultiLineEqual(test, ref, msg = "Rate file improperly written for two partitions, no het.")



    def test_evolver_twopart_nohet_seqfile(self):
        '''
            Test evolver with two partitions, no heterogeneity at all.
            Ensure leaf sequences only properly written to seqfile.
        '''
        evolve = Evolver(partitions = [self.part1, self.part2], tree = self.tree, seqfile = "out.fasta")()
        
        # Check seqfile, no ancestors
        aln = AlignIO.read("out.fasta", "fasta")
        os.remove("out.fasta")
        assert(len(aln) == 5), "Wrong number of sequences were written to file when write_anc=False."
        assert(len(aln[0]) == 22), "Output alignment incorrect length."
        

    def test_evolver_twopart_nohet_seqfile_anc(self):
        '''
            Test evolver with two partitions, no heterogeneity at all.
            Ensure ancestors properly written to seqfile.
        '''
        evolve = Evolver(partitions = [self.part1, self.part2], tree = self.tree, seqfile = "out.fasta", write_anc = True)()
        
        # Check seqfile, no ancestors
        aln = AlignIO.read("out.fasta", "fasta")
        os.remove("out.fasta")
        assert(len(aln) == 9), "Wrong number of sequences were written to file when write_anc=True."
        assert(len(aln[0]) == 22), "Output alignment incorrect length."
        
        
        




class evolver_sitehet_tests(unittest.TestCase):
    ''' 
        Suite of tests for evolver under temporally homogeneous conditions (no branch heterogeneity!!).
        Uses a single partition with nucleotides WITH site heterogeneity.
    '''
    
    def setUp(self):
        ''' 
            Tree and frequency set-up.
        '''
        self.tree = read_tree( tree = "(((t2:0.36,t1:0.45):0.001,t3:0.77):0.44,(t5:0.77,t4:0.41):0.89);" )
        f = EqualFrequencies(by = 'nuc')()
        
        m1 = Model()
        m1.params = {'state_freqs':f, 'mu':{'AC':1, 'AG':1, 'AT':1, 'CG':1, 'CT':1, 'GT':1}}
        m1.matrix = nucleotide_Matrix(m1)()
        m1.rates = [2.0783848 ,  0.89073634,  0.05938242]
        m1.probs = [0.33, 0.33, 0.34]
        self.part1 = Partition()
        self.part1.models = m1
        self.part1.size = 12
        
    def test_evolver_sitehet_ratefile(self):
        '''
            Test evolver with one partition, site heterogeneity.
            Ensure rate file correct.
        '''
        
        evolve = Evolver(partitions = self.part1, tree = self.tree, ratefile = "rates.txt")()
        # Check ratefile
        test = []
        with open('rates.txt', 'r') as test_h:
            for line in test_h:
                test.append(line)
        os.remove("rates.txt")
        assert( len(test) == 13 ), "Ratefile improperly written for single partition, site het (wrong num lines)."
        for i in range(1, 13):
            self.assertRegexpMatches( test[i], str(i) + "\t1\t[123]", msg = "Ratefile improperly written for single partition, site het (wrong line contents).")


    def test_evolver_sitehet_seqfile(self):
        '''
            Test evolver with one partition, site heterogeneity.
            Ensure leaf sequences only properly written to seqfile.
        '''
        evolve = Evolver(partitions = self.part1, tree = self.tree, seqfile = "out.fasta")()
        
        # Check seqfile, no ancestors
        aln = AlignIO.read("out.fasta", "fasta")
        os.remove("out.fasta")
        assert(len(aln) == 5), "Wrong number of sequences were written to file when write_anc=False."
        assert(len(aln[0]) == 12), "Output alignment incorrect length."
        

    def test_evolver_sitefile_seqfile_anc(self):
        '''
            Test evolver with one partition, site heterogeneity.
            Ensure ancestors properly written to seqfile.
        '''
        evolve = Evolver(partitions = self.part1, tree = self.tree, seqfile = "out.fasta", write_anc = True)()
        
        # Check seqfile, no ancestors
        aln = AlignIO.read("out.fasta", "fasta")
        os.remove("out.fasta")
        assert(len(aln) == 9), "Wrong number of sequences were written to file when write_anc=True."
        assert(len(aln[0]) == 12), "Output alignment incorrect length."







class evolver_branchhet_tests(unittest.TestCase):
    ''' 
        Suite of tests for evolver under branch heterogeneity.
        Uses a single partition with nucleotides *without* site heterogeneity.
    '''
    
    def setUp(self):
        ''' 
            Tree and frequency set-up.
        '''
        self.tree = read_tree( tree = "(((t2:0.36_m2_,t1:0.45):0.001,t3:0.77):0.44_m1_,(t5:0.77,t4:0.41):0.89);" )
        f = EqualFrequencies(by = 'nuc')()
        
        root = Model()
        root = Model()
        root.params = {'state_freqs':f, 'mu':{'AC':1, 'AG':1, 'AT':1, 'CG':1, 'CT':1, 'GT':1}}
        root.matrix = nucleotide_Matrix(root)()
        root.name = 'root_model'        
        
        m1 = Model()
        m1.params = {'state_freqs':f, 'mu':{'AC':1, 'AG':1, 'AT':1, 'CG':1, 'CT':1, 'GT':1}}
        m1.matrix = nucleotide_Matrix(m1)()
        m1.name = 'm1'
        
        m2 = Model()
        m2.params = {'state_freqs':f, 'mu':{'AC':1, 'AG':1, 'AT':1, 'CG':1, 'CT':1, 'GT':1}}
        m2.matrix = nucleotide_Matrix(m2)()
        m2.name = 'm2'      
        
        self.part1 = Partition()
        self.part1.models = [ m1, m2, root ]
        self.part1.size = 10
        self.part1.root_model = 'root_model'
        

    def test_evolver_branchhet_ratefile(self):
        '''
            Test evolver with one partition, branch heterogeneity.
            Ensure rate file correct.
        '''
        evolve = Evolver(partitions = self.part1, tree = self.tree, ratefile = "rates.txt")()
        # Check ratefile
        with open('evolFiles/single_part_no_het_rates.txt', 'r') as ref_h:
            ref = str(ref_h.read())
        with open('rates.txt', 'r') as test_h:
            test = str(test_h.read())
        os.remove("rates.txt")
        self.assertMultiLineEqual(test, ref, msg = "Rate file improperly written for single partition, no site het.")


    def test_evolver_sitehet_seqfile(self):
        '''
            Test evolver with one partition, branch heterogeneity.
            Ensure leaf sequences only properly written to seqfile.
        '''
        evolve = Evolver(partitions = self.part1, tree = self.tree, seqfile = "out.fasta")()
        
        # Check seqfile, no ancestors
        aln = AlignIO.read("out.fasta", "fasta")
        os.remove("out.fasta")
        assert(len(aln) == 5), "Wrong number of sequences were written to file when write_anc=False."
        assert(len(aln[0]) == 10), "Output alignment incorrect length."
        

    def test_evolver_sitefile_seqfile_anc(self):
        '''
            Test evolver with one partition, branch heterogeneity.
            Ensure ancestors properly written to seqfile.
        '''
        evolve = Evolver(partitions = self.part1, tree = self.tree, seqfile = "out.fasta", write_anc = True)()
        
        # Check seqfile, no ancestors
        aln = AlignIO.read("out.fasta", "fasta")
        os.remove("out.fasta")
        assert(len(aln) == 9), "Wrong number of sequences were written to file when write_anc=True."
        assert(len(aln[0]) == 10), "Output alignment incorrect length."
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
            
            

        
            
            
if __name__ == '__main__':
    run_tests = unittest.TextTestRunner()
    

    print "Testing evolver no het, one partition"
    test_suite0 = unittest.TestLoader().loadTestsFromTestCase(evolver_singlepart_nohet_tests)
    run_tests.run(test_suite0)

    print "Testing evolver no het, two partitions"
    test_suite1 = unittest.TestLoader().loadTestsFromTestCase(evolver_twopart_nohet_tests)
    run_tests.run(test_suite1)

    print "Testing evolver site het, one partition"
    test_suite2 = unittest.TestLoader().loadTestsFromTestCase(evolver_sitehet_tests)
    run_tests.run(test_suite2)
    
    print "Testing evolver branch het, one partition"
    test_suite3 = unittest.TestLoader().loadTestsFromTestCase(evolver_branchhet_tests)
    run_tests.run(test_suite3)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            