# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 13:49:26 2020

@author: gawehn
"""
import pdb

import matplotlib.pyplot as plt
import numpy      as np
import mat73
import pickle
import time

from collections  import namedtuple
from scipy.io     import loadmat
from scipy        import interpolate,integrate
from scipy.signal import detrend, hilbert
from matplotlib import path

from simple_utils import optional_print as op_print

class Data():
    def __init__():
        pass

    #@staticmethod
    def inpoly(xq, yq, xv, yv):
        shape   = xq.shape
        xq      = xq.reshape(-1)
        yq      = yq.reshape(-1)
        xv      = xv.reshape(-1)
        yv      = yv.reshape(-1)
        q       = [(xq[i], yq[i]) for i in range(xq.shape[0])]
        p       = path.Path([(xv[i], yv[i]) for i in range(xv.shape[0])])

        return p.contains_points(q).reshape(shape)

    def set_Video(X, Y, ImgSequence, m, n, l, dx, dt, label):
        VideoStruct     = namedtuple('struct', ['X', 'Y', 'ImgSequence', 'm', 'n', 'l', 'dx', 'dt', 'label'])
        Video           = VideoStruct(X, Y, ImgSequence, m, n, l, dx, dt, label)
        return Video

    def set_plot_limits(d_lims,diff_lims,err_lims):
        PlotLimStruct   = namedtuple('struct', ['d_lims', 'diff_lims', 'err_lims'])
        PlotLims        = PlotLimStruct(d_lims, diff_lims, err_lims)
        return PlotLims

    @classmethod
    def get_Video(cls,label, cam_name, startx = None, stopx = None, starty = None, stopy = None, step = None):
        op_print('load video data...', end =" ")
        start = time.time()
        if label == 'wavecams_palavas_cristal':
            if step is None: step = 1 #set default step
            frames_wavecams = np.load('/home/florent/dev/COCOS/data/raw/palavas/{cam_name}/20220314/07h/Video_compressed_palavas_{cam_name}_res_1.0.npz'.format(cam_name=cam_name))
            X           = frames_wavecams['X']
            Y           = frames_wavecams['Y']
            ImgSequence = frames_wavecams['RectMov_gray']
            dx          = frames_wavecams['dx']
            dt          = frames_wavecams['dt']
            d_lims      = [0, 8]
            diff_lims   = [-1.5, 1.5]
            err_lims    = [0, 1]
        if label == 'chicama':
            if step is None: step = 1 #set default step
            frames_wavecams = np.load('/home/florent/dev/COCOS/data/raw/chicama/{cam_name}/Video_compressed_chicama_{cam_name}.npz'.format(cam_name=cam_name))
            X           = frames_wavecams['X']
            Y           = frames_wavecams['Y']
            ImgSequence = frames_wavecams['RectMov_gray']
            dx          = frames_wavecams['dx']
            dt          = frames_wavecams['dt']
            d_lims      = [0, 15]
            diff_lims   = [-1.5, 1.5]
            err_lims    = [0, 1]
        if label == 'wavecams_palavas_cristal_merged':
            if step is None: step = 1 #set default step
            frames_wavecams = np.load('/home/florent/dev/COCOS/data/raw/palavas/{cam_name}/20220314/08hVideo_compressed_palavas_{cam_name}_res_1.0.npz'.format(cam_name=cam_name))
            X           = frames_wavecams['X']
            Y           = frames_wavecams['Y']
            ImgSequence = frames_wavecams['RectMov_gray']
            dx          = frames_wavecams['dx']
            dt          = frames_wavecams['dt']
            d_lims      = [0, 8]
            diff_lims   = [-1.5, 1.5]
            err_lims    = [0, 1]
        if label == 'wavecams_palavas_stpierre':
            if step is None: step = 1 #set default step
            frames_wavecams = np.load(f'/home/florent/dev/COCOS/data/raw/palavas/{cam_name}/20220323/15h/Video_compressed_palavas_{cam_name}.npz')
            X           = frames_wavecams['X']
            Y           = frames_wavecams['Y']
            ImgSequence = frames_wavecams['RectMov_gray']
            dx          = frames_wavecams['dx']
            dt          = frames_wavecams['dt']
            d_lims      = [0, 16]
            diff_lims   = [-1.5, 1.5]
            err_lims    = [0, 2]
        if label == 'duck': # define label
            if step is None: step = 1 #set default step
            DuckArgus   = loadmat('../data/Video_Duck.mat')
            X           = DuckArgus['XX']
            Y           = DuckArgus['YY']
            ImgSequence = DuckArgus['TimeStack']
            dx          = DuckArgus['dx'][0][0]
            dt          = DuckArgus['dt'][0][0]
            # only for visualization
            d_lims      = [0,6]
            diff_lims   = [-1.5,1.5]
            err_lims    = [0, 2]
        if label == 'scheveningen':
            if step is None: step = 1 #set default step
            SchevDrone  = np.load('../data/Video_Scheveningen.npz')
            X           = SchevDrone['X']
            Y           = SchevDrone['Y']
            ImgSequence = SchevDrone['RectMov_gray']
            dx          = SchevDrone['dx']
            dt          = SchevDrone['dt']
            # only for visualization
            d_lims      = [0,8]
            diff_lims   = [-1.5,1.5]
            err_lims    = [0, 2]
        if label == 'narrabeen':
            if step is None: step = 1 #set default step
            NarraDrone  = np.load('../data/Video_Narrabeen.npz')
            X           = NarraDrone['X']
            Y           = NarraDrone['Y']
            ImgSequence = NarraDrone['RectMov_gray']
            dx          = NarraDrone['dx']
            dt          = NarraDrone['dt']
            mask        = ~cls.inpoly(X,Y,np.array([341000,342400,342700,341000]),np.array([626700,6267200,6270000,6270000]))
            for ii in range(ImgSequence.shape[2]):
                ImgSequence[:,:,ii] *= mask
            # only for visualization
            d_lims      = [0,16]
            diff_lims   = [-1.5,1.5]
            err_lims    = [0, 2]
        if label == 'porthtowan':
            if step is None: step = 1 #set default step
            PortTArgus  = loadmat('../data/Video_Porthtowan.mat')
            X           = PortTArgus['X'][26:,:181]
            Y           = PortTArgus['Y'][26:,:181]
            ImgSequence = PortTArgus['ImgSequence'][26:,:181]
            dx          = PortTArgus['dx'][0][0]
            dt          = PortTArgus['dt'][0][0]
            mask        = ~cls.inpoly(X,Y,np.array([0,300,482,0]),np.array([580,580,-300,-300]))
            for ii in range(ImgSequence.shape[2]):
                ImgSequence[:,:,ii] *= mask
            # only for visualization
            d_lims      = [0,8]
            diff_lims   = [-1.5,1.5]
            err_lims    = [0, 2]
        if label == 'fig3':
            if step is None: step = 1 #set default step
            T   = 600
            dt  = 0.5
            m   = 128
            mult= m/128
            omegas   = np.array([1.75, 3.10, 1.0, 1.50, 4.2, 5.1])/2 #1.85
            IC  = np.array([0.5, -0.35, -0.70, -1.0, 0.55, 0.2])*m**2
            I   = (np.array([5, 6, 3, 5, 9, 12])*mult).astype(int)
            J   = (np.array([0, 3, 2, 2, 4, 5])*mult).astype(int)
            n   = int(T/dt)
            dx  = 1
            K   = 0 #reflection
            #factor needed for identical amplitudes between Fouerier spectra of progressive and (partly) standing wave fields
            elliptic_integral2ndkind = lambda x,K: (1-4*K/(K+1)**2*np.sin(x)**2)**0.5 #integral of amplitude (i.e. sqrt(1+2K*sin(2phi)+K**2)) in eq 10 of Goda & Suzuki 1976 (neglecting the scaling factor |1+K| in integral, which represents the added amplitude/excursion due to reflected component)
            itg_standWave   = integrate.quad(elliptic_integral2ndkind,a = 0,b = 2*np.pi, args=(K,))
            itg_progWave    = 1*2*np.pi
            fac             = itg_progWave/itg_standWave[0]
            [X,Y] = np.meshgrid(np.linspace(0,m-1,m),np.linspace(0,m-1,m))
            ImgSequence = np.zeros((m,m,n),dtype = float)
            for t_ID,t in enumerate(np.linspace(0,T,n)):# loop over time
                xtilde = np.zeros((m,m),dtype = 'complex128')
                for k in range(len(omegas)): # loop over waves
                    #wave incident
                    xtilde[I[k],J[k]] = np.exp(1j*omegas[k]*t)*(IC[k])*fac/(1+K)
                    #wave reflected
                    if J[k] == 0:
                        xtilde[m-I[k],0-J[k]] = np.exp(1j*omegas[k]*t)*(IC[k]*K)*fac/(1+K)
                    else:
                        xtilde[m-I[k],m-J[k]] = np.exp(1j*omegas[k]*t)*(IC[k]*K)*fac/(1+K)
                x = np.real(np.fft.ifft2(xtilde))
                ImgSequence[:,:,t_ID] = x

        ix_x  = slice(startx,stopx,step)
        ix_y  = slice(starty,stopy,step)
        m,n,l = ImgSequence[ix_y,ix_x,:].shape

        end = time.time()
        op_print('CPU time: {} s'.format(np.round((end-start)*100)/100))
        return Data.set_Video(X[ix_y,ix_x], Y[ix_y,ix_x], ImgSequence[ix_y,ix_x,:], m, n, l, dx*step, dt, label), Data.set_plot_limits(d_lims,diff_lims,err_lims)

    def get_GroundTruth(opts, Video, grid, step = None):
        op_print('   load ground truth data...', end =" ")
        start = time.time()
        if Video.label == 'wavecams_palavas_cristal':
            f_litto3d = '/home/florent/Projects/Palavas-les-flots/Bathy/litto3d/cristal/litto3d_Palavas_epsg_32631_775_776_6271.pk'
            # WL = 0.60 - 0.307 # 20220314 -07h/08h
            WL = 0.19 - 0.307 # 20220323 - 15h
            litto3d = pickle.load(open(f_litto3d, 'rb'))
            # plt.pcolor(litto3d['Xi'], litto3d['Yi'], litto3d['zi'], vmin=0, vmax=15)
            Z_groundTruth = interpolate.griddata((np.ravel(litto3d['Xi']), np.ravel(litto3d['Yi'])), np.ravel(litto3d['zi']),
                                                 (grid.X, grid.Y), method='linear')
            D_groundTruth = -1*Z_groundTruth+WL
        elif Video.label == 'wavecams_palavas_stpierre':
            f_litto3d = '/home/florent/Projects/Palavas-les-flots/Bathy/litto3d/st_pierre/litto3d_Palavas_st_pierre_epsg_32631_774_775_6270.pk'
            # WL = 0.60 - 0.307
            WL = 0.19 - 0.307
            litto3d = pickle.load(open(f_litto3d, 'rb'))
            # plt.pcolor(litto3d['Xi'], litto3d['Yi'], litto3d['zi'], vmin=0, vmax=15)
            Z_groundTruth = interpolate.griddata((np.ravel(litto3d['Xi']), np.ravel(litto3d['Yi'])), np.ravel(litto3d['zi']),
                                                 (grid.X, grid.Y), method='linear')
            D_groundTruth = -1*Z_groundTruth+WL

        elif Video.label == 'duck':
            WL              = 0.077
            CRABDuck        = loadmat('../data/GroundTruth_Duck.mat')
            [Xmeas,Ymeas]   = np.meshgrid(CRABDuck['xm'],CRABDuck['ym'])
            Z_groundTruth   = interpolate.griddata((np.ravel(Xmeas), np.ravel(Ymeas)), np.ravel(CRABDuck['zi']),(grid.X, grid.Y),method='linear')
            D_groundTruth   = -1*Z_groundTruth+WL
        elif Video.label == 'scheveningen':
            WL              = 0.6
            with open('../data/GroundTruth_Scheveningen.txt') as f:
                list_of_lists   = [[x for x in line.split()] for line in f]
                flattened_list  = [y for x in list_of_lists for y in x]
            bathydata   = np.array(flattened_list[19:]).astype('float')
            bathydata   = np.reshape(bathydata,(3, int(len(bathydata)/3)), order = 'F')
            bathyx  = bathydata[0,:]
            bathyy  = bathydata[1,:]
            bathyz  = bathydata[2,:]
            Z_groundTruth   = interpolate.griddata((bathyx, bathyy), bathyz,(grid.X, grid.Y),method='linear')
            D_groundTruth   = -1*Z_groundTruth+WL
        elif Video.label == 'narrabeen':
            # TO DOWNLOAD THE NARRABEEN GROUND TRUTH DATA:
            # Bathymetric validation data for this drone flight is kindly provided by the NSW Department of Planning, Industry and Environment (NSW DPIE, formerly NSW OEH). This data is available on the Australian Ocean Data Network (AODN) Data Portal. To access this data, do the following:
            # 1)            Click here on the following link:
            # https://catalogue-imos.aodn.org.au/geonetwork/srv/eng/catalog.search#/metadata/8b2ddb75-2f29-4552-af6c-eac9b02156a6
            # 2)            Click on “View and download data through the AODN portal”
            # 3)            To navigate to Narrabeen Beach, select the bounding box
            #                           N: --33.70
            #                           S: -33.74
            #                           E: 151.33
            #                           W: 151.29
            # 4)            At the bottom of the page, click “Next”
            # 5)            Click on the download link to download the dataset as a zip file. The relevant data file is
            # "NSWOEH_20170529_NarrabeenNorthenBeaches_STAX_2017_0529_Narrabeen_Post_ECL_No4_Hydro_Depths.xyz”
            # Note that this data is provided in EPSG 32756 (MGA94 Zone 56) and is referenced to Australian Height Datum (approximating MSL)
            # Put the downloaded file in the "data" directory
            WL              = 0.67
            with open('../data/NSWOEH_20170529_NarrabeenNorthenBeaches_STAX_2017_0529_Narrabeen_Post_ECL_No4_Hydro_Depths.xyz') as f:
                list_of_lists   = [line.split() for line in f]
                bathy_xyz       = np.array(list_of_lists, dtype = float)
            Z_groundTruth   = interpolate.griddata((bathy_xyz[:,0], bathy_xyz[:,1]), bathy_xyz[:,2],(grid.X, grid.Y),method='linear')
            D_groundTruth   = Z_groundTruth+WL
        elif Video.label == 'porthtowan':
            WL              = -0.96
            ErwinPortT      = loadmat('../data/GroundTruth_Porthtowan.mat')
            Xmeas,Ymeas     = ErwinPortT['Xi'],ErwinPortT['Yi']
            Z_groundTruth   = interpolate.griddata((np.ravel(Xmeas), np.ravel(Ymeas)), np.ravel(ErwinPortT['Zi']),(grid.X, grid.Y),method='linear')
            D_groundTruth   = -1*Z_groundTruth+WL
        else:
            op_print('No ground truth depth provided')
            D_groundTruth = np.nan
        # try:
        #     D_groundTruth[D_groundTruth<opts.dlims[0]] = np.nan
        # except:
        #     op_print('no gorund truth')

        end = time.time()
        op_print('CPU time: {} s'.format(np.round((end-start)*100)/100))

        return D_groundTruth
