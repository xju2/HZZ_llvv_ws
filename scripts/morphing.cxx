#include <TString.h>
#include <RooMomentMorph.h>
#include <iostream>

using namespace std;
bool exists(const std::string& name){
    ifstream f(name.c_str());
    return f.good();
}

RooHistPdf* get_pdf(RooWorkspace* ws, TH1F* h1, int mass, const char* ch_name)
{
    RooRealVar* x = (RooRealVar*) ws->var("x");
    RooDataHist datahist(Form("data_hist_%d_%s", mass, ch_name), "DH", RooArgList(*x), h1);
    RooHistPdf hist_pdf(Form("hist_pdf_%d_%s", mass, ch_name), "DH", RooArgSet(*x), datahist, 0);
    ws->import(hist_pdf);
    return (RooHistPdf*) ws->obj(Form("hist_pdf_%d_%s", mass, ch_name));
}

TH1F* get_hist(int mass, const char* prod, const char* channel){
    const char* input_dir= "/afs/cern.ch/user/x/xju/work/h4l/highmass/workspaces/LLVV/NWA_sameBinning/inputs";
    TFile* fin = TFile::Open(Form("%s/pdf_%s%d_all.root", input_dir, prod, mass));
    string hist_name(Form("mT-Nominal-%s", channel));
    TH1F* hist = (TH1F*) fin->Get(hist_name.c_str());
    hist->SetDirectory(0);
    fin->Close();
    return hist;
}

void make_morphed_hists(RooWorkspace* ws, const char* prod, int mass){
    string out_name(Form("inputs/pdf_%s%d_all.root", prod, mass));
    if (exists(out_name)) {
        cout << out_name <<" is there" << endl;
        return;
    }

    RooMomentMorph* morph_mm = (RooMomentMorph*) ws->obj("morph_mm");
    RooMomentMorph* morph_ee = (RooMomentMorph*) ws->obj("morph_ee");
    RooRealVar* mH = (RooRealVar*) ws->var("mH");
    RooRealVar* x = (RooRealVar*) ws->var("x");

    TFile* h_out = TFile::Open(out_name.c_str(), "recreate");

    mH->setVal(1.*mass);
    // mumu channel
    TH1F* h1 = (TH1F*) morph_mm->createHistogram("mT-Nominal-ggF_mmvv", *x, 
                RooFit::Binning(x->getBinning()));
    h1->SetName("mT-Nominal-ggF_mmvv");
    h1->Write();
    // ee channel
    TH1F* h1_ee = (TH1F*) morph_ee->createHistogram("mT-Nominal-ggF_eevv", *x, 
                RooFit::Binning(x->getBinning()));
    h1_ee->SetName("mT-Nominal-ggF_eevv");
    h1_ee->Write();

    // add VBF categories
    TH1F* h_VBF_ee = new TH1F("mT-Nominal-VBF_eevv", "VBF ee", 1, 0, 1500);
    TH1F* h_VBF_mm = new TH1F("mT-Nominal-VBF_mmvv", "VBF mm", 1, 0, 1500);
    h_VBF_ee->Write();
    h_VBF_mm->Write();

    h_out->Close();
}

void morphing(const char* prod = "ggH")
{
    gROOT->SetBatch();
    vector<int> masses = vector<int>();
    masses.push_back(300);
    masses.push_back(400);
    masses.push_back(500);
    masses.push_back(600);
    masses.push_back(700);
    masses.push_back(800);
    masses.push_back(900);
    masses.push_back(1000);
    masses.push_back(1200);

    RooWorkspace* ws = new RooWorkspace("combined", "combined");
    RooRealVar x("x", "x variable", 0, 1500);
    x.setBins(30);

    RooPlot* frame = x.frame();
    ws->import(x);

    RooArgList obs_list = RooArgList();
    obs_list.add(x);

    TVectorD param_vec = TVectorD((int)masses.size());

    RooRealVar mH("mH", "mH", 200., 2000.); 

    RooArgList pdfs_ee = RooArgList(); 
    RooArgList pdfs_mm = RooArgList(); 

    // vector<string> channels = {"ggF_mmvv", "ggF_eevv"};
    string ch_name("ggF_mmvv");
    string ch_ee("ggF_eevv");
    for(int ic = 0; ic < (int) masses.size(); ic++) {
        int mass = masses.at(ic);
        param_vec[ic] = mass;

        TH1F* h1 = get_hist(mass, prod, ch_name.c_str());
        RooHistPdf* pdf = get_pdf(ws, h1, mass, ch_name.c_str());
        pdf->plotOn(frame);
        pdfs_mm.add(*pdf);

        // ee channel
        TH1F* h1_ee = get_hist(mass, prod, ch_ee.c_str());
        RooHistPdf* pdf_ee = get_pdf(ws, h1, mass, ch_ee.c_str());
        pdfs_ee.add(*pdf_ee);
    }
    RooMomentMorph morph_mm("morph_mm", "morph", mH, obs_list, pdfs_mm, param_vec, 
            RooMomentMorph::Linear);

    RooMomentMorph morph_ee("morph_ee", "morph ee", mH, obs_list, pdfs_ee, param_vec, 
            RooMomentMorph::Linear);

    ws->import(morph_mm);
    ws->import(morph_ee);

    for(int t_mass = 300; t_mass <= 1200; t_mass += 10){
        make_morphed_hists(ws, prod, t_mass);
    }

    delete ws;
}
