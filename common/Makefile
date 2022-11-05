update-makefile:
	@mkdir -p common
	@curl https://raw.githubusercontent.com/sasano8/portfolio/main/common/Makefile -o common/Makefile

update-common:
	@curl https://raw.githubusercontent.com/sasano8/portfolio/main/common/mkdocs_base.yml -o common/mkdocs_base.yml
	@mkdir -p docs
	@mkdir -p docs/overrides
	@mkdir -p docs/overrides/css
	@curl https://raw.githubusercontent.com/sasano8/portfolio/main/docs/overrides/main.html -o docs/overrides/main.html
	@curl https://raw.githubusercontent.com/sasano8/portfolio/main/docs/overrides/print_site_banner.tpl -o docs/overrides/print_site_banner.tpl
	@curl https://raw.githubusercontent.com/sasano8/portfolio/main/docs/overrides/css/custom.css -o docs/overrides/css/custom.css
	@curl https://raw.githubusercontent.com/sasano8/portfolio/main/.editorconfig -o .editorconfig
	@curl https://raw.githubusercontent.com/sasano8/portfolio/main/.github/workflows/github_pages.yml -o .github/workflows/github_pages.yml
	@mkdir -p .vscode
	@curl https://raw.githubusercontent.com/sasano8/portfolio/main/.vscode/.gitignore -o .vscode/.gitignore

doc-build:
	@poetry run mkdocs build

doc-serve: doc-build
	@poetry run mkdocs serve -a localhost:8001

grep-todo:
	@grep -n -e "TODO:" -e "FIXME:" -r --exclude="Makefile" --exclude-dir=".venv" . || true

openapi-generator-list:
	@docker run --rm openapitools/openapi-generator-cli list
	# docker run --rm -u `id -u`:`id -g` -v ${PWD}:/local openapitools/openapi-generator-cli generate -g ${GENERATOR} -i /local/${INPUT} -o /local/${OUT}
	# autorestも試してみたい

format-sql:
	@sqlfluff fix --dialect postgres .
