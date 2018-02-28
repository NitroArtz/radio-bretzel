#Scripts organization

##scripts
- defaults.liq
    - what every scripts will do
- source\<SourceName>.liq
    - script called by the docker command, must create a faillible source named "source"
- createStream.liq
    - create a infaillible source from the source created by source\<SourceName>.liq
- outputStream.liq
    - choose which script from "/outputs/" to load from environment variable "STREAM_OUTPUT_TYPE"
- outputs/output\<OutputType>.liq
    - load datas from env if needed and stream out the "radio" stream created before

##source\<SourceName>.liq exemple
```
#!/usr/bin/liquidsoap
%include "includes/defaults.liq"

#your source creation logic
#must create a source variable containing the source

%include "includes/createStream.liq"

%include "includes/outputStream.liq"
````
