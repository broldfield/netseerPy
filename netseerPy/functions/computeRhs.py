# Compute RHS which takes in a graphlist, formulation, new_nodes, f_rhs_hi, f_hrs_lo, vertex, freq, total_hi, total_lo, and returns the RHS of the constraint.
import numpy as np
import pandas as pd


# Convert the compute_rhs function from the netseer r package to python
def computeRhs(
    graphList, formulation, newNodes, fRhsHi, fRhsLo, vertex, freq, totalHi, totalLo
):
    degree = newDegree = fRhs = rmVerts = signs = fRhs = dfTempRm = None
    match newNodes:
        case _ if newNodes > 0:
            newDegree = predictNewNodesDegree(graphList)
            if fRhsLo is None:
                fRhs = {fRhsHi, np.repeat(newDegree, newNodes)}
                signs = {np.repeat("<=", len(fRhsHi)), np.repeat("<=", newNodes)}
            else:
                fRhs = {
                    fRhsHi,
                    np.repeat(newDegree, newNodes),
                    fRhsLo,
                    np.repeat(0, newNodes),
                }
                signs = {
                    np.repeat("<=", len(fRhsHi)),
                    np.repeat("<=", newNodes),
                    np.repeat(">=", len(fRhsLo)),
                    np.repeat(">=", newNodes),
                }
        case 0:
            fRhs = {fRhsHi, fRhsLo}
            signs = {np.repeat("<=", len(fRhsHi)), np.repeat(">=", len(fRhsLo))}
        case _ if newNodes < 0:
            rmNum = -1 * newNodes
            signs = {np.repeat("<=", len(fRhsHi)), np.repeat(">=", fRhsLo)}

            dfTemp = pd.DataFrame(
                {
                    "vertex": vertex,
                    "degree": np.concatenate((fRhsHi, fRhsLo)),
                    "signs": signs,
                    "freq": freq,
                }
            )
            dfTempRm = (
                dfTemp.pipe(filterItem).pipe(arrangeItem).pipe(sliceItem, 0, rmNum)
            )

    if formulation == "max":
        fRhs = fRhs + freq
    else:
        fRhs = fRhs - freq
    if formulation == "max":
        fRhs = fRhs - totalHi
    else:
        fRhs = fRhs - totalLo
    return fRhs


def arrangeItem(df):
    return np.arrange(df)


def sliceItem(df, start, end):
    return np.slice(df, start, end)


def filterItem(df):
    return np.filter(df, degree == 0)
