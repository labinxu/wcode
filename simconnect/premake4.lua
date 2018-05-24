project "simconnect"
  configuration "Debug or Release"
    kind "SharedLib"

  configuration "UnitTest"
  kind "StaticLib"

  configuration {}
  linkoptions {"-Wl,--no-undefined" }
  links { "boost_thread-mt",
          "boost_system-mt",
          "pthread" }
  
  files { "*.cpp"}
