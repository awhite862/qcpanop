"""
Utility to convert pyscf mean-field objects to RDMs
"""
import numpy as np
from pyscf import gto, scf, ao2mo
from functools import reduce


def rhf_to_v2rdm(mf: scf.RHF, rdm_constraints: str):
    """
    Convert a RHF object from pyscf to call v2rdm object

    :param mf: scf.RHF object
    :param rdm_constraints: ['D', 'DQ', 'DQG', 'DG', 'DQGT']
    :return:
    """
    assert isinstance(mf, scf.rhf.RHF)
    # make h1 and spatial integrals in MO basis
    eri = ao2mo.kernel(mol, mf.mo_coeff)
    eri = ao2mo.restore(1, eri, mf.mo_coeff.shape[1])

    # this produces the unfolded spatial integrals in chemist notation
    # (11|22)
    print(eri.shape)  # this should be (mf.mo_coeff.shape[1],) * 4
    print(mf.mo_coeff.shape[1])

    # this produces spatial MO h1 integrals
    h1 = reduce(np.dot, (mf.mo_coeff.T, mf.get_hcore(), mf.mo_coeff))
    print(h1.shape)  # should (mf.mo_coeff.shape[1],) * 2

    # now either build k2 or use hilbert to run v2rdm with singlet case


def rohf_to_v2rdm(mf: scf.ROHF, rdm_constraint):
    """
    This should be the same integrals as RHF but spin will be different
    Remember mf.spin is equal to 2S NOT 2S + 1

    :param mf:
    :param rdm_constraint:
    :return:
    """
    assert isinstance(mf, scf.rohf.ROHF)
    # make h1 and spatial integrals in MO basis
    eri = ao2mo.kernel(mol, mf.mo_coeff)
    eri = ao2mo.restore(1, eri, mf.mo_coeff.shape[1])

    # this produces the unfolded spatial integrals in chemist notation
    # (11|22)
    print(eri.shape)  # this should be (mf.mo_coeff.shape[1],) * 4
    print(mf.mo_coeff.shape[1])

    # this produces spatial MO h1 integrals
    h1 = reduce(np.dot, (mf.mo_coeff.T, mf.get_hcore(), mf.mo_coeff))
    print(h1.shape)  # should (mf.mo_coeff.shape[1],) * 2

    neleca, nelecb = mf.nelec
    spin = mf.mol.spin
    multiplicity = spin + 1

    # ... run v2RDM


def uhf_to_v2rdm(mf: scf.UHF, rdm_constraint):
    assert isinstance(mf, scf.uhf.UHF)
    # EXTRACT Hamiltonian for UHF
    norb = mf.mo_energy[0].size
    mo_a = mf.mo_coeff[0]
    mo_b = mf.mo_coeff[1]

    # this builds the h1a and h1b components
    h1e_a = reduce(np.dot, (mo_a.T, mf.get_hcore(), mo_a))
    h1e_b = reduce(np.dot, (mo_b.T, mf.get_hcore(), mo_b))

    # this builds the aa, ab, bb two electron integral blocks
    g2e_aa = ao2mo.incore.general(mf._eri, (mo_a,)*4, compact=False)
    g2e_aa = g2e_aa.reshape(norb,norb,norb,norb)
    g2e_ab = ao2mo.incore.general(mf._eri, (mo_a,mo_a,mo_b,mo_b), compact=False)
    g2e_ab = g2e_ab.reshape(norb,norb,norb,norb)
    g2e_bb = ao2mo.incore.general(mf._eri, (mo_b,)*4, compact=False)
    g2e_bb = g2e_bb.reshape(norb,norb,norb,norb)

    # OPTIONAL this is how I would put it into OpenFermion Order.
    # See PQRS convention in OpenFermion.hamiltonians._molecular_data
    # h[p,q,r,s] = (ps|qr)
    g2e_aa_of = np.asarray(1. * g2e_aa.transpose(0, 2, 3, 1), order='C')
    g2e_bb_of = np.asarray(1. * g2e_bb.transpose(0, 2, 3, 1), order='C')
    g2e_ab_of = np.asarray(1. * g2e_ab.transpose(0, 2, 3, 1), order='C')

    neleca, nelecb = mf.nelec
    spin = mf.mol.spin
    multiplicity = spin + 1

    # .. run v2RDM


if __name__ == "__main__":
    mol = gto.M()
    mol.atom = '''N 0 0 0; N 0 0 1.6'''
    mol.basis = 'cc-pvtz'
    mol.charge = 0
    mol.spin = 0
    mol.build()

    mf = scf.RHF(mol)
    mf.verbose = 4
    mf.kernel()
    rhf_to_v2rdm(mf, 'DQG')


    mol = gto.M()
    mol.atom = '''O 0 0 0; O 0 0 1.6'''
    mol.basis = 'cc-pvtz'
    mol.charge = 0
    mol.spin = 2
    mol.build()

    mf = scf.ROHF(mol)
    mf.verbose = 4
    mf.kernel()
    rohf_to_v2rdm(mf, 'DQG')


    mf = scf.UHF(mol)
    mf.verbose = 4
    mf.kernel()
    uhf_to_v2rdm(mf, 'DQG')



