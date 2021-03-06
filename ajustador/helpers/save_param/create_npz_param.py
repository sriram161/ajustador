"""
@Description: Primary execution module to generate modified param_cond.py and
              morph_file.p based on the conductance parameters present in npz file.
@Author: Sri Ram Sagar Kappagantula
@e-mail: skappag@masonlive.gmu.edu
@Date: 5th Mar, 2018.
"""

import logging
import numpy as np
from pathlib import Path
from ajustador.helpers.loggingsystem import getlogger
from ajustador.helpers.save_param.process_common import create_path
from ajustador.helpers.save_param.process_npz import get_least_fitness_params
from ajustador.helpers.save_param.process_npz import get_conds_non_conds
from ajustador.helpers.save_param.process_common import get_file_abs_path
from ajustador.helpers.save_param.process_npz import make_cond_file_name
from ajustador.helpers.save_param.process_common import process_modification

logger = getlogger(__name__)
logger.setLevel(logging.INFO)

def create_npz_param(npz_file, model, neuron_type, store_param_path=None,
                     fitnum=None, cond_file= None):
    """Main function to be executed to generate parameter file from npz_file.
       Inputs => *.npz file; model can be 'gp', 'd1d2', 'ep' or 'ca1' soon;
                 neuron_type can be 'proto', 'D1' or 'D2' soon;
                 store_param_spath is user intended path to store neuron parameter files;
                 fitnum is user desired fitnumber to extract from npz file;
                 cond_file= Pure file name no path prefixes,
       Note** Program searches for cond_file in model folder and conductance_save in-order.
    """
    import moose_nerp
    model_path = Path(moose_nerp.__file__.rpartition('/')[0])/model

    logger.info("START STEP 1!!!\n loading npz file: {}.".format(npz_file))
    data = np.load(npz_file)

    logger.info("START STEP 2!!! Prepare params.")
    fit_number, param_data_list = get_least_fitness_params(data, fitnum)
    header_line = "# Generated from npzfile: {} of fit number: {}\n".format(
                  npz_file.rpartition('/')[2], fit_number)
    logger.debug("Param_data: {}".format(param_data_list))
    conds, non_conds = get_conds_non_conds(param_data_list)

    new_param_path = create_path(store_param_path) if store_param_path else create_path(model_path/'conductance_save')
    if cond_file is None:
        cond_file = 'param_cond.py'
    new_param_cond = make_cond_file_name(data, npz_file,
                         str(new_param_path), neuron_type, cond_file)

    process_modification(new_param_cond, model_path, new_param_path,
                         neuron_type, fit_number, cond_file, model,
                             conds, non_conds, header_line)
