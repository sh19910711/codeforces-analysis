tmp:
	mkdir tmp

stack: tmp
	aws cloudformation package \
		--template-file cloudformation.yaml \
		--s3-bucket codeforces-analysis \
		--s3-prefix cloudformation \
		--output-template-file tmp/packaged-cloudformation.yaml

	aws cloudformation deploy \
		--template-file tmp/packaged-cloudformation.yaml \
		--stack-name codeforces-analysis \
		--capabilities CAPABILITY_IAM

s3bucket:
	aws s3 mb s3://codeforces-analysis
