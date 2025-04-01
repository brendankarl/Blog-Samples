import oci

config = oci.config.from_file()

def transcribe(inputfile,compartmentid,bucket,namespace):
    ai_speech_client = oci.ai_speech.AIServiceSpeechClient(config)
    create_transcription_job_response = ai_speech_client.create_transcription_job(
            create_transcription_job_details=oci.ai_speech.models.CreateTranscriptionJobDetails(
                compartment_id=compartmentid,
                input_location=oci.ai_speech.models.ObjectListInlineInputLocation(
                    location_type="OBJECT_LIST_INLINE_INPUT_LOCATION",
                    object_locations=[oci.ai_speech.models.ObjectLocation(
                        namespace_name=namespace,
                        bucket_name=bucket,
                        object_names=[inputfile])]),
                output_location=oci.ai_speech.models.OutputLocation(
                    namespace_name=namespace,
                    bucket_name=bucket)))

transcribe(inputfile="Name of file to transcribe",compartmentid="OCID of the compartment to run the transcription job in",bucket="Bucket that contains the file to transcribe",namespace="Object storage namespace")
