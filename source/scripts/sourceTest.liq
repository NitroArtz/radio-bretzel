#!/usr/bin/liquidsoap
%include "includes/defaults.liq"

source = playlist("/audio/")

%include "includes/createStream.liq"

%include "includes/outputStream.liq"
