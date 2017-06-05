#include <TString.h>
#include <RooMomentMorph.h>

RooHistPdf* get_pdf(RooWorkspace* ws, TH1F* h1, int mass)
{
    RooRealVar* x = (RooRealVar*) ws->var("x");
    RooDataHist datahist(Form("data_hist_%d", mass), "DH", RooArgList(*x), h1);
    RooHistPdf hist_pdf(Form("hist_pdf_%d", mass), "DH", RooArgSet(*x), datahist, 0);
    ws->import(hist_pdf);
    return (RooHistPdf*) ws->obj(Form("hist_pdf_%d", mass));
}

string get_hist_name(int mass, const char* channel){
    if (mass > 1000){
        return Form("VBFH%dNW_mT_%s___Cut0", mass, channel);
    } else{
        return Form("VBF%dNW_mT_%s___Cut0", mass, channel);
    }
}

void morphing(){
    const char* file_name = "/afs/cern.ch/user/m/mpetrov/public/Combination_work_Updated/VBF_Signals/VBF_Signals_ggH.root";
    TFile* f1 = TFile::Open(file_name);
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
    x.setBins(100);

    RooPlot* frame = x.frame();
    ws->import(x);

    RooArgList obs_list = RooArgList();
    obs_list.add(x);

    TVectorD param_vec = TVectorD((int)masses.size());

    RooArgList pdfs = RooArgList(); 
    RooRealVar mH("mH", "mH", 200., 2000.); 

    for(int ic = 0; ic < (int) masses.size(); ic++) {
        int mass = masses.at(ic);
        TH1F* h1 = (TH1F*) f1->Get( get_hist_name(mass, "ee").c_str() ); 
        RooHistPdf* pdf = get_pdf(ws, h1, mass);
        pdf->plotOn(frame);
        pdfs.add(*pdf);
        param_vec[ic] = mass;
    }
    RooMomentMorph morph("morph", "morph", mH, obs_list, pdfs, param_vec, 
            RooMomentMorph::Linear);
    morph.Print("v");

    TFile* h_out = TFile::Open("out_hist.root", "recreate");

    for(int ic = 1; ic < (int) masses.size(); ic++) {
        float mass = (masses.at(ic-1) + masses.at(ic))/2.0;
        mH.setVal(mass);
        morph.plotOn(frame, RooFit::LineColor(kRed));
        TH1F* h1 = (TH1F*) morph.createHistogram(Form("h_%.f", mass), x, 
                RooFit::Binning(x.getBinning()));
        h1->SetName(Form("h_%.f", mass));
        h1->Write();
    }
    h_out->Close();

    c1 = TCanvas();
    frame->Draw();
    c1.SaveAs("test.pdf");

    delete ws;
    f1->Close();
}
