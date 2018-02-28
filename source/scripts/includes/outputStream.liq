output_type = getenv('STREAM_OUTPUT_TYPE')

if output_type == "icecast"
   then
   %include "outputs/outputIcecast.liq"
else
   %include "outputs/outputDummy.liq"
   end
