#include <iostream>
#include <G4UIExecutive.hh>
#include <memory>
#include <G4ios.hh>

int main(int argc, char** argv)
{
  std::unique_ptr<G4UIExecutive> ui;

  if(argc ==1)
    ui.reset(new G4UIExecutive(argc,argv));

  G4cout << "initialized UI executive" << G4endl;

  //TODO: test whether data files can be found?
}
